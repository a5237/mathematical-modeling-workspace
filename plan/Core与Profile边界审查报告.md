# Core 与赛事 Profile 边界审查报告

> 审查对象：`refactor/multi-contest-core`（`ee26a06`）的 Core 全量；`feature/mcm-icm-profile`（`d1e4dc7`）的美赛适配只读取证（`git show`/`git diff`），本分支不含 `config/contests/mcm-icm/`。
>
> 判据与步骤见 `plan/Core与Profile边界审查执行方案.md`。本轮只判定边界，不改规范、不动 T3–T12。

## 一、结论

1. **机器层最干净，散文层最不干净。** 45 个 Core 契约键中只有 3 个的取值是赛事的（`body_word_minimum`、`body_page_minimum`、`body_page_maximum`），1 个混入赛事交付物（`release_core_files` 的 `08-delivery/file-list.md`），2 个的统计范围需随口径外移（`body_figure_minimum`/`body_table_minimum`）；其余 39 个是工作区机制。而"隐性 CUMCM 化"集中在 `paper-writing.md` §3、`paper-formatting.md` §1.4、`paper-quality-audit.md` §4/§8 的自然语言与 `audit_modeling_project.py` 的代码常量里。上一次的抽象只把**数字**参数化了，没有把**口径、编号样式、交付集、章节名**参数化。
2. **抽象轴选错了一半。** 现有分层用的是"官方规定 vs 工作区增补"，不是"跨赛事 vs 单赛事"。单赛事时期两者等价，双赛事后不等价：**工作区自设的国赛形状**（CUMCM 的章节结构与节名、关键词 4–6 个、5000 字口径、file-list）既不冒充官方、也不跨赛事，正好落在旧判据的盲区——这是根因。
3. **Profile 的语义被理解成"官方规则快照"，但需要外移的多半不是官方规则。** `body_page_*` 下沉进 `rules.md` 是权宜：页数上限是官方的，页数下限和字数下限是工作区自设的，写进"官方基线"文件与该文件自己的使用规则（"不得冒充官方统一要求"）冲突。修法是**在同一 `rules.md` 内分两段、各带一个机器契约块**（§A 官方条款，`last_verified` 只覆盖本段；§B 本赛事下的工作区设定），加载器已支持同文件多块并禁止块间重名键，零代码改动。**不分文件**：官方值与工作区设定都是这个赛事专属的规则，同处一套 profile 文件；分段只为一个维护动作服务——`last_verified` 与提交前重核官方只覆盖官方段，内部门禁不进重核范围。非官方条目实数只有 4 个数值加约 6 条散文，为它们增设权威落点会引入"两边都能写规则"的漂移面。
4. **接入第二个赛事的真实代价已可量化，且每一处都是 Core 侧的条件句。** `git diff refactor/multi-contest-core feature/mcm-icm-profile` 显示 8 个 Core 文件被改动，其中 4 处是边界缺陷（见 §5.4）。
5. **`paper-writing.md` §3 固定的是国赛那篇论文的骨架，而不是"论文有骨架"这件事。** 证据：摘要页加正文七节加附录这套结构只出现在 Core 散文和 CUMCM 的 `.tex` 里，两套 `rules.md` 都没有记录它，CUMCM 官方快照只写到"摘要专用页含标题、摘要和关键词"（`config/contests/cumcm/rules.md:18`）。它是许多师生默认的 CUMCM 论文格式约定，本身正当；错在把单一赛事的约定当成跨赛事通用规范写进 Core——下沉进 profile 即取得权威，不需先补官方出处。
6. **`paper-figures.md` 和两个 Skill 是正确分层的样板**：只有纪律、字段、状态枚举和解析链，零赛事数字，零语言形状。修 Core 的方向就是把其余论文规范改成这个形状，而不是再加配置项。
7. **最隐蔽的一处不在条文里，在代码常量里**：占位符检测词表只有中文（`audit_modeling_project.py:38`），因此每个从 CUMCM 模板复制来的 `main.tex` 因注释里的"占位"必报假 MAJOR，而英文论文的未填字段一个都检不出（P12）。以"搜不到 CUMCM 字样"为通过标准的审查必然漏掉它——同理，`profile.yaml` 只有三个字段这一事实也不含任何赛事字样，却是所有下沉无处可去的根因（P13、P15）。

## 二、Core 应当是什么（从零重述）

从零设计一个不认识任何赛事的建模工作区，仍然必须存在的能力只有四类：

| # | Core 职责 | 本仓库的承载 | 现状 |
|---|---|---|---|
| C1 | 生命周期与导航：inbox→project→archive、00–08 阶段职责、`sandbox/` 边界、产物地图、影响传播、状态枚举 | `workspace-governance.md`、`workspace-layout.md`、`trace-artifact-impact.py` | 基本干净 |
| C2 | 可信性机制：数据不可变与复现、运行/日志/种子、主张-证据-文献契约、验证义务、AI 使用台账 | `data-reproducibility.md`、`evidence-contract.md`、`modeling-execution.md`、`WG-AI-001` | 干净，只欠措辞中性化 |
| C3 | 论证纪律：数学化—求解—回答—验证闭环、章节**职责与顺序**、图表的论证职责、不得以排版或堆砌掩盖缺失内容 | `paper-writing.md` §2/§5–§10、`paper-figures.md` | §3/§4/§11/§12 混入赛事形状 |
| C4 | 可覆盖默认值 + 契约机制本身：中性锚点、Core 键闭集、profile 解析链、"官方未规定时如此" | `control_contracts.py`、`docs/README.md` 矩阵、`AGENTS.md` | 机制正确，闭集只允许换数字 |

配套两条硬判据，后续所有条目按此裁决：

- **文字系统判据**：Core 的硬性要求必须能写成对任一文字系统都可执行的形式——该文字不存在时条款**空转**，不算违反。按文字系统分派的规则（汉字→宋体、拉丁与数字→Times 系、变量斜体）与带"官方未规定时"前提的默认值（A4、字号、缩进、行距、图内 9 pt、300 dpi）都通过此判据，留 Core；只有"在另一文字系统下照做反而错"的无条件 Mandate 才下沉——一级标题必须用"一、"（`paper-formatting.md:61`）、一级标题必须居中（`:63`）。
- **权威归属判据**：一条规则的**存在理由**若只能由某赛事官方文件给出，或它是对官方约束的本地化取值，则它必须能在 profile 内找到唯一归属；Core 不得留"下方为中文赛事的实现，其它赛事……"这类条件句（美赛分支 `paper-writing.md:125` 正是被禁的形态）。

## 三、主要边界问题

| ID | 问题 | 证据 | 为什么是边界问题 |
|---|---|---|---|
| P1 | Core 固定了国赛章节名与编号，而非章节职责 | `paper-writing.md:127-188`、`:196`"一级章节的名称、顺序和职责固定"、`:192` 字数口径写作"问题重述→模型的评价与推广" | 节名与"一、"编号是 CUMCM 的默认形状（官方未逐条规定，师生与评阅惯例如此）；MCM 官方只规定 Summary Sheet 在首页、正文/参考文献/附录顺序。英文论文无法满足"名称固定" |
| P2 | 度量口径留在 Core，值已下沉 | `paper-quality-audit.md:148`（本分支写死 20—30 页与起止定义）、`:209-212` 报告字段 `body_page_range/body_page_count`；美赛分支只把数值改成 profile 键 | "body=正文=摘要页后到参考文献前"本身是国赛概念。口径不随值走，同一键名在两套 profile 下含义相反（正文段 vs 全 PDF），机器读对数字读错语义 |
| P3 | 交付集写死在 Core，含机器锁 | `paper-quality-audit.md:21` `release_core_files` 含 `08-delivery/file-list.md`；`workspace-layout.md:20` `08-delivery/support-materials` 在推荐骨架里；`artifact-map.yaml:13,15` 把 `paper`/`delivery` 索引分别绑到 `main.tex` 与 `file-list.md`；`tools/tests/test_v2_smoke.py:129-130` 断言每个推荐目录必须存在 | 单一 PDF 的赛事既没有支撑材料也不允许额外文件；四处独立执行点（契约键、骨架数组、模板索引、测试断言）+ `trace-artifact-impact.py:156-194` 的阶段名推断，使交付集变更无法只落在 profile 一层 |
| P4 | 排版条款要分三类判，不能整块下沉 | §1.2 字体分派表（`:28-36`）、§1.3 字号与段落（`:40-57`）、§1.4 编号与对齐（`:61-63`） | ① **按文字系统分派**的条款（"全部中文字符用宋体"、拉丁与数字用 Times 系、变量斜体）在英文论文下命中集合为空，属空转不是违反，**留 Core**；② §1.1/§1.3 带"官方或赛区未规定时"前提，属可覆盖默认值，**留 Core**；③ 只有 §1.4"`一级标题使用'一、'`"与"一级标题居中"是无条件 Mandate 且英文照做即错，**下沉** |
| P5 | Profile 只能表达标量，结构/语言/交付集无处可放 | `profile.yaml` 仅 `contests`/`contract_keys`/`paper_framework`；`control_contracts.py:331-344` 只做键集合相等校验 | 于是结构事实唯一的落点是 `.tex`，模板变成隐性权威：美赛 `paper-framework.tex` 写死"25 页"4 处，改一届要改 4 行，Core 又重复一遍同一形状规则 → 双写漂移 |
| P6 | 语料层无归属承载，且资源文件自成第二权威 | `resources/paper-library/` 的 `01/02/03` 按 CUMCM 题号注释绑题号；`00-format-layout/` 本分支未分区；`00-format-layout/README.md:24` 在资源库里重述"中文用宋体、英文用 Times"；`resources/algorithm-library/03-评价类算法说明.md:2517` 出现"国赛第二问"；`pre-writing-learning.md:6` `learning_paper_minimum=2` 是 Core 键 | 门禁机制是 Core，样本是按赛事的语料。三层模型（Core/Profile/Project）没有"按赛事打标的资源"这一类，只能靠目录约定和散文点名赛事（美赛分支 `pre-writing-learning.md:27` 已点名 CUMCM/MCM-ICM）。语料目录同时开始复述规范，形成第二权威 |
| P7 | Core 内已出现条件豁免句与失效引用 | `paper-formatting.md:21`"培训展示型 Word 框架…不自动继承""中文学位论文的横向页面需求" | `resources/templates/` 下不存在任何 Word 框架（仅 `README.md`、`artifact-map.yaml`、`figure-selection-record.md`、`contests/`）。这是对话历史残留，不是跨赛事机制 |
| P8 | 闭集校验只允许"加新键"，不允许改 Core 键的适用范围 | `control_contracts.py:337` profile 不得重定义 Core 键、`:315-323` Core 键闭集 | 表达力上限=换数字。凡"同一指标不同口径""同阶段不同交付物"都只能改 Core，于是必然出现 `audit_modeling_project.py` 式的 optional 分支 |
| P9 | 匿名性条款缺"官方要求的标识必须出现"这一半 | `paper-writing.md:594`、`workspace-layout.md`/`data-reproducibility.md:101` 只禁止身份暴露 | CUMCM 电子版第一页不含编号专用页，MCM 却要求每页页眉含队控制号。只写禁令会漏掉"官方要求携带的标识按官方位置出现"，两条同时成立才是通用规则 |
| P10 | Core 把"论文 = 一个 LaTeX 单文件"当成通用事实，连 CUMCM 自己都不满足 | `naming.md:29-30` 固定 `06-paper/main.tex`、`paper-quality-audit.md:20` `release_core_files` 要求 `main.tex`、`artifact-map.yaml:13` `paper: 06-paper/main.tex` | 本 profile 的官方快照明写"电子论文为单个 PDF **或 Word** 文件"（`cumcm/rules.md:20`）。走 Word 交付时 Core 门禁必然判缺失；`profile.yaml` 的 `paper_framework` 也是单值字符串（`control_contracts.py:199-200`），无法表达"两篇文档/非 LaTeX"。这是最承重的一条隐性假设 |
| P11 | AI 交付形态从 profile 回渗进 Core | `workspace-governance.md:146`"从台账生成当届要求的**声明和详情文件**" | "声明 + 独立详情 PDF"是 CUMCM 的两件套（`cumcm/rules.md:39-41`）；MCM 是行内引用 + 文末一节。台账机制是 Core，输出物名称不是 |
| P12 | **中文词表被写进机器逻辑**：占位符检测只认中文 | `audit_modeling_project.py:38` `PLACEHOLDER = TODO\|TBD\|FIXME\|待填写\|待补\|占位\|XX+`，在 release 阶段作用于 `06-paper/main.tex`（`:370-372`） | 双向失效，均已实证：初始化即复制的 CUMCM 模板正文注释含"占位"（`contests/cumcm/paper-framework.tex:3,113,128`，`:136` 还有 `\textbf{图像占位}`）→ 每个新项目 RC 必报假 MAJOR；英文模板未填的 `\TemplateField{…}` 渲染为 `[...]`，一个词都不命中 → 真漏检。**这是隐性 CUMCM 化最纯的形态：不在规范条文里，而在代码常量里，因此搜"CUMCM"永远搜不到** |
| P13 | Profile 只能提供**值**，永远不能提供**检查** | `control_contracts.py:336-338` 禁止重定义 Core 键；`final_audit_fields/pass_fields/zero_fields` 是 Core 闭集（`paper-quality-audit.md:24-46`），审校脚本只遍历这三个集合 | MCM 官方要求每页页眉 `Team # , Page n of 25`、CUMCM 要求支撑材料内含 `AI 工具使用详情.pdf`——两者都无法成为门禁。这是"接入新赛事必须改 6 个 Core 文件"的结构性原因，而不只是条目遗漏。同时 Core 硬读 profile 键 `contracts.paper_maximum_bytes`（`audit:379`）却无必需键下限，空 profile 能通过校验再到 RC 崩 |
| P14 | 交付物字节上限单值，双制品赛事漏检 | `audit:375-379` 只 glob `08-delivery/*.pdf` 并与 `paper_maximum_bytes` 比较 | CUMCM 实际有两个制品（论文 ≤20 MB + RAR/ZIP ≤20 MB，`cumcm/rules.md:20-21`），压缩包无任何机器检查；"08-delivery 恰好一个 PDF"对 MCM 是巧合正确 |
| P15 | 审校无条件执行 `PW-FMT-001`，不跳过对当前论文不适用的条款 | `modeling-paper-audit/SKILL.md:20`；`paper-formatting.md:9` 已声明"首先服从官方基线" | `paper-formatting.md` 没有机器契约块不构成缺陷：排版的下沉落点是 `rules.md` §B 段。真正的问题是执行侧——§1.4 两条单语言 Mandate 在英文论文上必产伪 finding，随 P4 下沉后自动消失，不需要新增跳过逻辑 |

## 四、判定

### 4.1 保留在 Core（含"来自 CUMCM 但从零仍成立"）

| 内容 | 证据 | 保留理由（从零判据） |
|---|---|---|
| 00–08 阶段**集合**与 `sandbox/` 例外 | `workspace-layout.md:6-22`、`:86-109` | 读题→数据→模型→结果→证据→写作→审校→交付是建模活动的通用形状，与任何赛事官方无关 |
| 产物分类、影响传播、状态枚举 | `workspace-governance.md:12-55` | 纯工作区机制 |
| 数据不可变、环境锁定、运行/日志/种子、稳定产物复现 | `data-reproducibility.md` 全文 | 任何赛事的"可复算"要求都依赖它 |
| 主张/证据/文献三本台账与核验状态 | `evidence-contract.md` | 跨赛事，且官方无法豁免 |
| AI 台账机制与"从台账生成当届声明、不得凭记忆补写" | `workspace-governance.md:138-146` | 记录机制通用，委托方向正确；但同一条把 CUMCM 的"声明+详情文件"两件套写进了 Core 措辞，需按 P11 中性化 |
| 提交前重核官方来源 + 中性锚点引用 | `paper-writing.md:25`、`docs/README.md` profile 路由行 | 抽象方向正确，保持 |
| 字体分派表（汉字→宋体系、拉丁与数字→Times 系、变量斜体、图表内同规则、代码等宽、不嵌字体文件、同级标题加粗一致） | `paper-formatting.md:28-36` | 每条都按文字系统分派，英文论文下汉字条款空转而非被违反；从零写一份中西混排规范也会是这个形状 |
| §1.3 字号与段落默认值（小四/五号/行距/缩进） | `paper-formatting.md:40-57` | 以"官方或赛区未规定时"为前提，属 C4 可覆盖默认；只需把字号名表达成制度无关（中文字号或等价 pt） |
| 表题在上、三线表、不截图插表、跨页重复表头、单位与有效数字、公式不图片、禁止缩字号压行距凑门禁 | `paper-formatting.md:70-79`、`:87-153` | 语言与纸张无关的呈现纪律 |
| 图型三级决策、模型原生结构优先、色标/误差/`n` 披露、9 pt、300 dpi、PDF+PNG | `paper-figures.md` 全文 | 本工作区最干净的规范，作为其余论文规范的形状基准 |
| 长度/图/表"必须有下限量化门槛"这件事 | `paper-quality-audit.md:146-147` | 从零设计同样会设防"薄论文"的最低线；下沉的是**取值与口径**，不是**这条纪律** |
| 参考文献 ≥6 篇 + 至少 1 本教材类方法学来源且正文实际引用 | `paper-writing.md:546-557`（去掉两本指定书名后） | 工作区质量线，非官方要求 |
| 竞争力评分六维量表 | `paper-quality-audit.md:162-182` | 维度（理解与假设/创造性与适配/结果与证据/表达与视觉/求解与复现/完成度）跨赛事成立；只去掉"国奖/全国/一等奖"字样 |
| A4 纵向单栏、边距≥官方、页码阿拉伯数字页脚居中、不设装饰页眉 | `paper-formatting.md:18-23` | 均以"官方未规定时"为前提，属可覆盖默认值；美赛模板改用 `letterpaper` 与页眉页码是**应在 profile 声明的偏离**，不构成 Core 缺陷 |
| AI 台账七列 `ai_log_columns` | `workspace-governance.md:19` | 逐字看是 CUMCM 2026 条款（`cumcm/rules.md:41`）的镜像，但在 MCM 政策下同样可满足（工具与模型、目的与环节、提示方式、采纳、人工修改、核验），因此按文字系统判据留 Core；它的来源是历史，不是约束 |
| `01-problem`/`03-models`/`07-review` 三阶段的产物名（问题核对清单、模型选择记录、审稿台账） | `workspace-layout.md:89-105` | 不因 CUMCM 评阅表形态而存在，任何赛事的建模过程都需要这三件事；不得因"国赛也有"而下沉 |

### 4.2 下沉 Profile

| 内容 | 证据 | 归属段 | 判据 |
|---|---|---|---|
| 论文章节结构与节名 | `paper-writing.md:127-188`、`:196` | `rules.md` §B 段（结构要求），`paper-framework.tex` 是其实现 | P1：Core 固定职责与顺序即可；同时把 `.tex` 当权威会让模板升级成第三权威，正是 P5 的成因 |
| 字数下限取值与统计口径 | `paper-writing.md:10`、`:192` | 工作区设定段 | P2/P8；计数法（汉字/英文词/数字串各 1）留 Core |
| 页数上下限**口径**（哪一段被计、什么不计页） | `paper-quality-audit.md:148`；美赛分支已下沉值未下沉口径 | 官方快照（上限）+ 工作区设定（下限/口径） | P2 |
| 图表数下限的**统计范围**（"正文"定义） | `paper-quality-audit.md:147` | 工作区设定段 | 值可留 Core，范围随 P2 同因 |
| 报告字段 `body_*` 命名 | `paper-quality-audit.md:24-44`、`:204-220`、`audit_modeling_project.py:97-124` | Core 改赛事中性名（`counted_*`），口径由 profile 声明 | P2：名字本身携带国赛"正文"概念 |
| `release_core_files` 中的 `08-delivery/file-list.md` | `paper-quality-audit.md:21` | 拆 Core 集 + profile 交付集 | P3 |
| `08-delivery/support-materials` 骨架目录 | `workspace-layout.md:20`、`README.md:61-63` | profile 交付集声明 | P3 |
| 一级标题编号样式"一、"与一级标题居中 | `paper-formatting.md:61`、`:63` | §B 工作区设定段 | P4③：无条件 Mandate 且英文照做即错；字体与字号不在此列（见 §4.1） |
| 关键词个数与分隔符（存在性属官方，已在 `cumcm/rules.md:18`） | `paper-writing.md:131`、`:256-262`、`paper-formatting.md:47` | §B 工作区设定段 | MCM Summary Sheet 无关键词概念；结构要求归 §B，`.tex` 是实现 |
| 承诺书/编号专用页、"赛区"、支撑材料清单措辞、附件包格式 | `cumcm/rules.md:20-22`、`paper-writing.md:29`、`:590`、`:594` | 官方快照 | 纯官方条款，位置已正确 |
| 两本指定中文教材 | `paper-writing.md:548-553`、`:568` | 官方快照外的 CUMCM 设定段 | 用户已定 |
| 样本库题号映射（A→物理机理、B/D→运筹、C/E→统计） | `resources/paper-library/README.md` 目录注释 | profile 语料映射；类目标签保持按方法命名 | P6：类目跨赛事有效，题号映射无效 |
| 页眉必须含队控制号一类"官方要求携带的标识" | MCM 侧 `rules.md:16` | 官方快照 | P9 的另一半；`00-admin/project.yaml` 与 `<contest>-<year>-<problem>` 语法都没有承载官方标识符的位置，需 profile 声明标识槽 |
| 论文载体与篇数（LaTeX 单文件 vs Word vs 摘要页/Summary Sheet 独立成篇） | `naming.md:29-30`、`paper-quality-audit.md:20`、`artifact-map.yaml:13`、`control_contracts.py:199-200` | profile 载体声明（`paper_framework` 由单值改为带角色的列表） | P10；Core 只留"论文有唯一权威源、可编译或可导出为交付件"这件事 |
| AI 输出物名称与位置（声明节 / 详情文件 / 行内引用+报告节） | `workspace-governance.md:146` | 官方快照 | P11；台账列留 Core |

### 4.3 待判断（需外部事实或实测校准，不在本轮定死）

| 项 | 缺的事实 | 影响 |
|---|---|---|
| MCM 是否要求独立 "Conclusion" 节 | 2027 届 COMAP Instructions 原文（美赛 `rules.md:30` 来源） | 决定 §3 职责序列里"回答与局限"是否单列，不能为迁就模板改 Core |
| 英文论文的叙述性长度线 | 需要 2 篇真实 25 页 MCM 获奖论文的叙述字数分布 | 决定 `body_word_minimum` 在 mcm-icm 是取低值、不设、还是改用其它代理指标 |
| 报告字段里 `final_pdf`、`08-delivery/paper.pdf` 等 PDF 载体假设 | 是否存在非 PDF 载体的赛事 | 若长期只有 PDF 交付，保持现名，不做预防性改名（`figure_final_pdf_statuses` 因无消费者已在 R1 删除，不属此项） |
| 第三赛事（非中非英、或无线上提交） | 无样本 | 只在出现时验证 profile 承载是否够用，本轮不为它设计 |

## 五、哪些是"先 CUMCM 后抽象"造成的

1. **判据错位**（§一.2）。抽象时问的是"这条会不会随年度/官方变"，所以只有**会变的事实**（页数、字节、载体、AI 条款）被搬走；**看起来像"论文本身"的形状**（节名、关键词、摘要页、正文/附录二分、支撑材料）被认为不会变，留在了 Core。这些形状对另一赛事既非"年度变化"也非"官方冲突"，只是不存在。
2. **抽象方向是"给 CUMCM 加参数"，不是"定义一套接口"**。`CORE_REQUIRED_KEYS` 是闭集、profile 禁止重定义 Core 键（`control_contracts.py:337`）——这个设计能防漂移，但也就把 profile 的表达力上限钉在"同一条规则换个数字"（P8）。
3. **锚点先行、内容未动**。`OFFICIAL-CUMCM-001` 的中性化改的是**引用写法**（`paper-writing.md:25`、`:579`、`paper-formatting.md:9`），做得干净；被引用的**内容层**（§3 结构、§1.2–1.4 排版、§4.3 口径）未做同构改写，于是形成"引用已通用、正文仍专用"的半成品状态。
4. **美赛分支的 8 处 Core 改动是这套历史观的账单**，其中 4 处属边界缺陷、需在重排后以"下沉"而非"加条件句"重做：
   - `control_contracts.py` 从 Core 闭集删 2 键 → 键的归属变了，但**方向正确**（值本就是赛事的）；
   - `audit_modeling_project.py:99-101,115-122` 新增 `getattr` 缺省与三态区间措辞 → Core 代码为单赛事缺项加分支，P8 的症状；
   - `paper-writing.md:125` 追加"下方为中文赛事（CUMCM）的实现；其它赛事……" → **被禁形态**，须由 §4.2 第 1 行的结构下沉替代；
   - `pre-writing-learning.md:27` 在 Core 散文里点名两个赛事的样本目录 → 应改为按 profile 解析的路径模板，语料归属见 P6。
   
   另外 2 处属正当修复（`paper-quality-audit.md:148` 口径委托、`:3` 国奖→获奖），2 处属导航（`docs/README.md`、`test_audit_refactor.py`）。
5. **模板成为第三权威**。profile 只有 `.tex` 一个结构承载物（P5），所以结构既写在 Core §3，又写在模板，还写在 profile 散文里；美赛模板 4 处写死页数、`\pageref{LastPage}` 把不计页的 AI 节算进页眉总页数，都是"没有槽位只能写在模板里"的后果。
6. **profile 只被设计成装"官方快照"，没有装工作区约定的位置。** 于是 CUMCM 那套默认的论文格式（章节结构、节名、编号样式）既进不去 profile、又不该留在 Core，就留在了 Core（§一.5）。这类条目不需要官方出处来背书，它需要的是 profile 内"本赛事工作区约定"的位置——即 §B 段；R1 补位置，R2 搬条目。同一原因也让 `body_page_minimum`、`body_word_minimum`、5 图 3 表、关键词个数、两本教材这些内部门禁无处可放。

## 六、后续重构顺序的调整建议

顺序原则：**先定 Core 的形状，再扩 Profile 的承载，最后才搬数值与措辞。** 已验证不可行的反序是"先下沉数值再逐条补"——`body_page_*` 下沉后，口径、交付集与节名仍卡在 Core，每接入一个赛事就必须在 Core 加一处例外。

**本轮范围决定**：本分支只把 CUMCM 从 Core 分离进 profile，不建美赛 profile、不做只有美赛才需要的官方标识槽；论文结构要求归 profile 的 §B 段，`paper-framework.tex` 是实现。落地细则见 `plan/Core与Profile边界审查执行方案.md` §2–§6。

| 阶段 | 做什么 | 完成判据 | 与现有 T 系列 |
|---|---|---|---|
| R0 Core 正面定义 | 把 §二 的 C1–C4 与两条判据写成 `docs/standards/workspace-governance.md` §1 的一节"分层判据"（≤20 行），并在 `docs/README.md` 加 profile 分段职责行 | 任何一条"要不要下沉"的争论可用两条判据一次裁决，不再逐条表决 | **取代 T4 总则**（T4 只说"冲突即下沉"，未给 Core 的正面定义） |
| R1 Profile 承载 | 同一 `rules.md` 内分 §A 官方条款段（`last_verified` 只覆盖此段）与 §B 本赛事工作区设定段，各带一个机器契约块（加载器已支持多块，零代码改动）；§B 承载五类：**论文章节结构与节名**、内部长度线与口径（`body_page_minimum`、`body_word_minimum`、5 图 3 表取值）、标题编号样式与对齐、交付集（`extra_delivery_directories`、`extra_release_files`）、样本库路径与题型映射；代码侧只加类型化访问器与必需键的显式报错，`release_core_files` 拆 Core∪profile；Core §3 只留职责与顺序，`.tex` 作为 §B 结构的实现 | 新增赛事时 Core 文件零改动；profile 加键不需改 Core 类型名单；`rules.md` 段级作用域使"提交前重核官方"只针对 §A | 吸收 **T10** 全部、**T8**、**T9 的模板硬错**（T9 原列"可并行先做"，应改到 R1 之后）；**不做**载体多值化与官方标识槽（美赛独有，留 feature 侧验证） |
| R2 内容迁移 | 按 §4.2 逐条下沉；Core 对应段落改写为职责/中性名；`body_*` 字段改名并同步 §8 报告模板、审计脚本、测试 | Core 不含赛事专名、不含"一级标题用'一、'"这类单语言 Mandate、不含条件豁免句；字体分派表按文字系统表述（允许出现"中文字符""宋体"作为分派目标）；P1–P4、P7、P9 关闭 | 吸收 **T5**（范围已缩到 §1.4 两条）、**T7**、**T6**（T6 结论修正为"纪律留 Core、值与口径下沉"，见 §4.1/§4.2） |
| R3 语料打标 | `paper-library` 类目按方法命名保留，题号映射与赛事归属进 `rules.md` §B；`PWL-GATE-001` 改为按 profile 解析同赛事样本路径模板 | 学习门禁不再点名任何赛事 | 收 **T1/T2** 的残留（`00-format-layout` 分区、`01`–`03` 注释）与 P6 |
| R4 回归参数化 | 测试按 profile 表驱动（本分支只有 `cumcm` 一项，合并后自动覆盖 `mcm-icm`）：各自断言骨架、交付集、口径；Core-only 断言不含赛事专名与单语言 Mandate | `--contest` 取任一已声明赛事都走通；新增赛事只需新增 profile + 一条表项 | 吸收 **T12**，并修正 `test_v2_smoke.py:129-130` 把国赛骨架断言为通用骨架 |
| R5 官方重核 | 美赛提交前重核 COMAP Instructions/AI 政策；把 §4.3 两项待判断落成事实 | `last_verified` 与生效日期更新 | 即 **T3**，属 feature 侧内容，与本层重构解耦、不排队 |

一句风险提示：R1 之前不要做任何 Core 文案改写——T5/T6/T7 的条目在 R1 未完成时落地，只能以"塞进 `rules.md` §A 官方条款段"为形式，那会把工作区自设值冒充成官方条款，制造比现状更难发现的新边界错误。

### 对现有 T3–T12 条目的修正

| 条目 | 修正 | 依据 |
|---|---|---|
| T5 | 结论方向对但**范围判重了**。它列的"中文字符宋体、加粗宋体、小四/五号、首行缩进、A4、页脚页码"要么按文字系统分派（英文下空转不构成违反），要么带"官方未规定时"前提（可覆盖默认），**都留 Core**；实际只需下沉 §1.4 的编号样式与标题对齐两条。落点是 `rules.md` §B 段，不需要先给 `paper-formatting.md` 补机器契约 | P4、§4.1 |
| T6 | 修法与 T4 自相矛盾：T4 禁止 Core 例外，T6 却把 `getattr` optional 分支当作目标设计。按 §4.1/§4.2，长度**纪律**留 Core、值与口径下沉，Core 代码不需要 optional 分支 | §4.1、P2 |
| T8 | 止于"标题措辞 profile 化"。真正承重的是三处机器锁：`release_core_files` 列了 `file-list.md`、`recommended_project_directories` 造了 `support-materials/`、`artifact-map.yaml:15` 把 `delivery` 索引绑到该文件。只改标题改不掉必然存在的双文档交付物假设 | P3、§4.2 |
| T9 | 保留，但整体后移到 R1 之后：模板的两处硬错（LastPage 计入 AI 节、AI 报告被排成 Appendix B）根源是"页数与节角色在模板里硬编码"，R1 提供键与角色槽后一次改对，否则重复修 | §5.5 |
| T10/T11/T12 | 吸收进 R1/R4；T12 需增加一条断言：`test_audit_refactor.py:62-83` 当前把"长度与图表预算是 Core 键"当作被测事实写死，R2 落地时该断言本身要改 | §六 R4 |

### 本轮新增、T 系列未覆盖的缺陷

1. **P12 中文词表进代码**——搜索"CUMCM"永远找不到它，且双向失效已实证。
2. **P13 profile 无法声明检查**，只能声明值；且 Core 硬读 profile 键却无必需键下限。这是"新赛事必须改 Core"的根因，T4 只给了原则没给机制。
3. **P14 双制品字节上限**——压缩包（`cumcm/rules.md:21`，官方值）无任何机器检查，"08-delivery 恰好一个 PDF"对美赛是巧合正确。
4. **P15 审校无条件执行 `PW-FMT-001`**——修法是下沉 §1.4 两条，不给 `paper-formatting.md` 补机器契约。
5. **死键**：`figure_final_pdf_statuses` 被 `CORE_REQUIRED_KEYS` 强制并做类型校验，全仓库无任何消费者（只出现在 `control_contracts.py:73,116`）→ 45 键闭集不是由机器需要推导的，扩槽前应先按消费者清点。
6. **跨 profile 脆弱**：`resolve_profile`（`control_contracts.py:213-216`）为解析一个赛事会加载全部 profile，且 `available_contests()` 出现在"未知赛事"的报错路径里（`:328`）→ 任一 profile 损坏会让所有赛事的身份解析失败。

## 七、本轮范围外

`docs/`、`tools/`、`.codex/`、`config/`、模板与测试均未改动；T3–T12 未执行、未改写；未提交、未推送。所有 `file:line` 均在当前工作树或指定 ref 的 blob 上直读复核。
