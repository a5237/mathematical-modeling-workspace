# Core 与赛事 Profile 边界 · 判定与执行方案

> 范围：本分支只把 CUMCM 的具体事实从 Core 分离进赛事 profile。架构判定与其证据见 `plan/Core与Profile边界审查报告.md`。

## 0. 前提

- 工作树：分支 `refactor/multi-contest-core`（`ee26a06`），`config/contests/` 只有 `cumcm`。
- `mcm-icm` profile、美赛论文框架、4 篇美赛范文与 T3–T12 待办在 `feature/mcm-icm-profile`（`d1e4dc7`）。本轮不建、不改这些内容；需要核对美赛事实时用 `git show <ref>:<path>` 只读取，不切分支。
- 为便于日后两分支合并：沿用 feature 已确立的 profile 目录、键名与 `resources/templates/contests/cumcm/paper-framework.tex` 路径；替换它的两处被禁形态（`audit_modeling_project.py` 的 `getattr` optional 分支、`paper-writing.md:125` 的条件句）；`国奖→获奖` 两侧同名改动应自动合并。
- 美赛内容侧缺陷（其模板 `\pageref{LastPage}` 把不计页的 AI 节算进页眉总页数、AI 报告被排成 Appendix B、"25 页"写死 4 处）只存在于 feature 分支的文件，另开一轮处理。
- 美赛自己的章节结构（Summary Sheet 首页、正文、参考文献、附录、不计页的 Report on Use of AI 附加节）由 feature 侧在 `config/contests/mcm-icm/` 的 §B 段写；本轮不预测其内容。

## 1. 判据

主判据：**今天从零设计一个完全不知道 CUMCM 的数学建模工作区，这条规则是否仍然必须存在。**

拆成四个子问，任一为"是"即归 Profile：

| 子问 | 含义 | 反例（仍属 Core） |
|---|---|---|
| Q1 官方性 | 该规则的存在理由是否只能由某一赛事官方文件给出？ | "提交前重核官方来源"本身是通用的 |
| Q2 语言/文字 | 在另一文字系统下**照做反而错**的无条件条款（一级标题用"一、"、一级标题必须居中） | 按文字系统分派、在英文下空转的条款（汉字→宋体、拉丁与数字→Times 系）；带"官方未规定时"前提的默认值（A4、字号、缩进、行距） |
| Q3 载体 | 是否依赖特定提交载体或交付集（单个 PDF / RAR 附件包 / 支撑材料清单）？ | "交付件不得暴露身份" |
| Q4 度量口径 | 数值可参数化，但**统计口径本身**是否由赛事定义？ | 复现、证据、命名、生命周期机制 |

配套原则：

- **默认值 vs 硬要求**：Core 可保留"官方未规定时"的可覆盖默认值；不得保留在另一赛事下方向相反的硬要求。
- **职责 vs 名称**：Core 固定"这一节回答什么问题、按什么顺序出现"；节名、编号样式、是否单列由 profile 承载。
- **机制 vs 语料**：门禁机制与按赛事打标的参考语料是两件事，语料既不是 Core 规则也不该被 Core 写死。
- **段 vs 文件**：官方性与工作区设定的区别由**段与契约块**承载。新载体物只在"同一文件内的分段会让某个维护动作的作用域失效"时才成立。
- **单一承载物**：一条事实只允许一个权威落点。论文结构的权威落点是当前 profile 的 §B 段，`paper-framework.tex` 是它的**实现**；Core 只固定"这一节回答什么、按什么顺序出现"，不复述任何单一赛事的节名。
- **赛事约定不必须有官方出处**：一条规则只要是该赛事下的工作区约定，profile 就是它的权威；不必先证明官方规定过它才能下沉，也不必留在 Core 冒充通用。

三分类：`Core`（保留）/ `Profile`（下沉）/ `待判断`（需外部事实或实测校准）。

## 2. R0 Core 正面定义

`docs/standards/workspace-governance.md` §1 新增控制编号 `WG-LAYER-001`（≤20 行）：Core 四类职责（生命周期与导航 / 可信性机制 / 论证纪律 / 可覆盖默认值与契约机制）+ §1 的 Q1–Q4 判据。`docs/README.md` 与 `AGENTS.md` 补 profile 分段职责行，并删去"当前唯一 profile"这类随分支失效的措辞。

判据：任何"要不要下沉"的争论可用 Q1–Q4 一次裁决，不再逐条表决。

## 3. R1 profile 承载

赛事专属的规则一律写进 `config/contests/cumcm/rules.md`，不分文件；文件内分两段、各带一个 `toml machine-contract` 块（加载器已支持同文件多块并禁止块间重名键，零代码改动）。分段只为一个维护动作服务：`last_verified` 与提交前重核只覆盖 §A。

- **§A 官方条款**：含 `paper_maximum_bytes`、`archive_maximum_bytes`（支撑材料压缩包 ≤20 MB，`rules.md:21`）、`body_page_maximum`（正文 ≤30 页）、载体与摘要页条款、AI 声明形态、匿名性官方清单。
- **§B 本赛事下的工作区设定**：**论文章节结构**（摘要页含关键词，正文七节按序为问题重述、问题分析、模型假设、符号说明、模型的建立与求解、模型的评价与推广、参考文献，其后附录；每问的预备条件独立成 `5.x.1` 小节）、`body_page_minimum`（20）、`body_word_minimum`（5000）及其口径、关键词个数、两本指定教材、标题编号样式与对齐、样本库路径与题型映射、`extra_delivery_directories`、`extra_release_files`。编号图与编号表的下限不在此列：2026-09-27 经语料核验升为 Core 统一值 `body_figure_minimum = 5`、`body_table_minimum = 2`，落在 `docs/standards/paper-quality-audit.md` §4 的契约块。依据是 4 篇美赛 O 奖论文的不同图号为 12/15/19/19、不同表号为 2/3/5/5——图、表的**个数**不依赖文字系统与统计口径，可通用；国赛原设的 3 表高于美赛最薄样本，故通用线取 2 而不是把 3 搬进 Core。

`rules.md` 现"使用规则"段（`:51`）随之外提：它写着"论文内容、通用排版与图片要求由 Core 在本官方基线上增补"，改后 §B 条目由本文件自持、Core 只引用不复述。

代码侧：

1. `profile.yaml` 的 `contract_keys` 随 §B 扩容。
2. Core 的三个类型名单只管 Core 键；profile 键由消费点经类型化访问器（`contract_int`/`contract_str`/`contract_list`）读取，缺键抛明确 `ContractError`。这同时消掉 Core 直接读 `contracts.paper_maximum_bytes`（`audit_modeling_project.py:379`）导致空 profile 到 RC 才崩的问题。
3. `release_core_files` 拆为 Core 集与 profile 集，审校取并集；`recommended_project_directories` 去掉 `08-delivery/support-materials`，改由 `extra_delivery_directories` 提供；初始化器按 profile 建目录与交付清单。
4. 删除无消费者的 Core 键 `figure_final_pdf_statuses`（`control_contracts.py:73,116` 声明并校验，全仓库无读取点）。

不做：新开 profile 文件、约束对象 schema、`paper_framework` 多值化、Word 载体支持（记为已知限制）、官方标识槽（美赛独有，留 feature 侧验证）。

## 4. R2 内容迁移

按报告 §4.2 逐条执行，字体分派表整块留 Core。

- `paper-writing.md`：§3 结构职责化（Core 只留"这一节回答什么、按什么顺序"的职责表；上面那套 CUMCM 章节结构整体移入 `rules.md` §B，由 `contests/cumcm/paper-framework.tex` 继续实现）、§3.1 长度口径改职责锚点、§4.1 标题句式、§4.4 关键词、§11.1 两本教材、§12.2 附录、§12.3 匿名性清单、`:118` 缩写条款改通用式。
- `paper-formatting.md`：仅 §1.4 的编号样式与一级标题对齐移 §B；`:21` 对不存在的 Word 框架的引用删除。
- `paper-quality-audit.md`：`body_*` 报告字段改 `counted_*`，同步 §8 报告模板、审校脚本与测试；§4.3 口径委托 §B。
- `workspace-governance.md:146`："声明和详情文件"改中性表述，具体输出物名归 §A。
- `data-reproducibility.md:101`、`workspace-layout.md:107`、`README.md:61-63` 的"支撑材料"措辞随交付集改写。
- `resources/paper-library/00-format-layout/README.md:24` 改为引用 `PW-FMT-001`；`resources/algorithm-library/03-评价类算法说明.md:2517` 的"国赛第二问"改中性。
- **占位符检测**：`audit_modeling_project.py:38` 的 `main.tex` 检查由中文词表改为结构标记——两套模板都以 `\TemplateField{...}` 表示未填（`contests/cumcm/paper-framework.tex:114`），图缺失标记用其宏名；`TODO|TBD|FIXME` 保留，中文词表只用于 `00-admin/` 等记录文件。

## 5. R3 语料归属

`paper-library` 的方法学类目命名不动，A/B/C/D/E 题号映射移入 §B；`00-format-layout/` 先分区为 `cumcm/`（与 feature 同向）；`pre-writing-learning.md` 写成两条赛事无关纪律——结构学习只计同赛事样本、样本目录按当前 profile 解析——数值 `learning_paper_minimum` 移 §B。

## 6. R4 回归

- `test_audit_refactor.py:62-83` 按 profile 取键；`test_v2_smoke.py:129-130` 的目录断言按 profile 骨架。
- 新增 Core 纯净性守卫：`docs/` + 通用模板 + Core 代码不含 `cumcm|国赛|赛区|支撑材料|一、`，以及不含条件豁免句。它是下限守卫，不是判据。
- 基准：`load_workspace_contracts(root, "cumcm")` 逐键 diff 为空，改名与迁移键先列白名单，白名单外任何差异即回退。
- 每步跑 `.venv-modeling/Scripts/python.exe -m pytest tools/tests -q` 与 `tools/check-workspace-layout.py`。

## 7. 提交切分与约束

`R0 定义` → `R1 承载` → `R2 论文族迁移` → `R3 语料` → `R4 测试`，共 5 个提交，逐个跑测试。不自动 commit、不 push，每步待授权。

全程不以"搜不到 CUMCM 字样"作为通过标准；不为任一赛事在 Core 写条件豁免句；不执行、不改写 T3–T12。
