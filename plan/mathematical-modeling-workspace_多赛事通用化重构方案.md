# 数学建模工作区多赛事通用化重构方案

## 总目标

当前 `mathematical-modeling-workspace` 底层设计以 CUMCM 为主，现需逐步重构为：

> **通用数学建模生产内核 + 赛事规则/模板适配层**

首批支持：

- CUMCM（全国大学生数学建模竞赛）
- MCM/ICM（COMAP 美赛）

后续可在不改动通用内核的情况下继续增加其它数学建模赛事。

### 核心原则

1. 通用流程只保留一次，不因赛事复制整套规则。
2. 赛事差异通过赛事配置、规则和模板表达。
3. **不新增不必要的 Skill**；优先改造现有 Production / Audit Skill，使其读取当前项目赛事配置。
4. 保留当前 CUMCM 工作流的成熟能力，不因通用化降低原有功能。
5. Agent 自主判断 `inbox` 中题目所属赛事，不单独建立“赛事识别 Skill”或复杂分类系统；识别后再加载相应赛事规则。
6. 不要为了“统一”而强行抹平赛事之间真实存在的差异。
7. 赛事官方规则始终高于工作区默认规则；工作区只抽象真正通用的原则和生产流程。

---

# 第一阶段：全量盘点并提取通用部分

## 目标

先明确哪些内容本质上属于“数学建模生产”，哪些只是当前 CUMCM 的实现。

**本阶段暂不进行大规模移动、重命名或删除，先完成耦合盘点和拆分设计。**

## 1.1 建立 CUMCM ↔ MCM/ICM 共性矩阵

对当前工作区重要规范、Skill、工具、模板，以及 machine contract 中的每一个 key 逐项检查，结合 MCM/ICM 官方规则，按语义判定归属；不得按文件、目录或“是否出现 CUMCM 字样”判断。

五档归属：

- `Core`：跨数学建模赛事稳定成立；
- `Workspace Default`：工作区内部质量标准，非任何赛事官方要求；
- `Contest Profile`：赛事官方要求及赛事特定参数与语义；
- `Contest-shaped heuristic`：表面通用、实际带有特定赛事假设；
- `Project-local`：当前项目自己的决定。

三档粗标签 `CORE` / `MIXED` / `CONTEST-SPECIFIC` 保留为“是否需拆分”的快速标注：`CORE` 对应 `Core`，`CONTEST-SPECIFIC` 对应 `Contest Profile`，`MIXED` 必须进一步落到 `Workspace Default`、`Contest-shaped heuristic` 或 `Contest Profile` 之一，不得停留在 `MIXED`。

重点检查：

```text
workspace-governance
data-reproducibility
modeling-execution
evidence-contract
paper-writing
paper-formatting
paper-figures
pre-writing-learning
paper-quality-audit
naming
artifact-map
artifact-impact
sandbox
通用 tools
Production Skill
Audit Skill
论文模板
图表模板
AI 使用要求
匿名性要求
提交要求
```

最终形成一份：

```text
CUMCM / MCM-ICM 共性与差异矩阵
```

明确每项内容最终：

```text
保留在 Core
移动到 contest profile
拆分为 Core + Contest
重新设计
暂时保持兼容
```

矩阵同时给出五档归属与证据坐标（文件:行）；machine contract 键按 key 单独列出，并标注同键在不同赛事的语义与统计口径是否一致。

---

## 1.2 提取真正的通用数学建模流程

重点识别中国数学建模赛事与 MCM/ICM 都成立的共同生产过程，例如：

```text
题目理解
    ↓
问题拆解
    ↓
数据 / 题面分析
    ↓
模型选择
    ↓
数学模型建立
    ↓
算法与代码实现
    ↓
正式求解
    ↓
结果分析
    ↓
模型验证
    ↓
敏感性 / 稳健性 / 误差等适当分析
    ↓
证据整理
    ↓
论文表达
    ↓
最终审查
    ↓
交付
```

以下原则也优先考虑抽到通用 Core：

- 原始数据与正式结果可追溯；
- 模型、代码、参数和结果保持一致；
- 重要数值必须有证据来源；
- 论文不能脱离实际计算结果；
- 模型必须进行适用的验证；
- 外部资料和文献需要核验与引用；
- AI 使用必须真实披露并进行必要的人工作核验；
- 正式交付需要保证匿名性和材料完整性；
- 实验结果与正式结果分离；
- 上游正式产物变化后需要判断下游影响；
- 不能把工程记录、临时结果和过程状态直接当作论文内容。

这些内容应逐渐从“CUMCM 工作区规则”提升为：

> **通用数学建模工作区 Core。**

---

## 1.3 识别当前 CUMCM 耦合点

重点记录所有直接写死 CUMCM 的内容，例如：

```text
CUMCM 官方规则
CUMCM 页数限制
CUMCM 摘要页
CUMCM AI 声明格式
CUMCM AI 详情文件要求
CUMCM 支撑材料要求
CUMCM 特定匿名要求
CUMCM 特定提交要求
CUMCM 论文固定结构
CUMCM LaTeX 模板
CUMCM 初始化器
CUMCM Production Skill 名称与路径
CUMCM Audit Skill 名称与路径
CUMCM 年度规则引用
控制编号 `OFFICIAL-CUMCM-001` 的定义位置与全部跨文件引用
machine contract 中带赛事语义的键（如 PDF 体积上限、页数上限与计页口径）
```

最终形成：

```text
CUMCM 耦合点清单
```

作为第二阶段拆分依据。

---

# 第二阶段：构建赛事配置，并分离赛事专属内容

## 目标

让正式项目首先确定：

> **当前项目属于哪一个数学建模赛事。**

之后 Production、Audit、Template、Submission 等行为根据赛事配置加载对应规则。

---

## 2.1 扩展项目赛事身份，不新增独立身份源

`00-admin/contest.yaml` 不作为独立身份源。`00-admin/project.yaml` 已包含 `contest`、`year`、`problem`、`status`、`random_seed`，因此扩展该文件记录当前项目使用的 Contest Profile：

```text
项目只引用并选择 profile，不重复定义赛事规则。
```

字段对应关系：原方案的 `contest_family` 对应 `profile`，`contest_variant` 对应 `contest`。

建议增加的字段：

```yaml
profile: cumcm
```

例如 CUMCM：

```yaml
project_id: cumcm-2027-a
contest: cumcm
year: 2027
problem: a
profile: cumcm
status: intake
```

例如 MCM：

```yaml
project_id: mcm-2027-a
contest: mcm
year: 2027
problem: a
profile: mcm-icm
status: intake
```

- `contest` 与项目目录前缀 `<contest>-<year>-<problem>` 保持一致；
- `profile` 是 profile 目录键，允许与 `contest` 不同（如 `mcm` 与 `icm` 共用 `mcm-icm` profile）；
- 识别与核验结论的留痕按 `WG-EVID-001` 处理，不在 `project.yaml` 另建台账。

具体字段以最终架构设计为准，不要为了配置形式增加没有实际用途的字段。

---

## 2.2 Agent 负责赛事识别

`workspace/inbox/` 中出现新赛题时：

```text
读取题目与附件
    ↓
Agent 判断赛事
    ↓
核对官方来源
    ↓
确认赛事身份
    ↓
创建正式项目
    ↓
写入 00-admin/project.yaml 的 contest / profile
    ↓
加载对应赛事 Profile
    ↓
启动通用 Production 流程
```

不新增：

```text
contest-identification Skill
contest-classification Skill
```

也不需要复杂的自动分类器。

Agent 可以依据：

- 题目标题；
- 主办单位；
- 官方网址；
- 题目编号；
- 提交规则；
- 文件要求；
- 论文语言；
- Summary / 摘要要求；
- AI 使用要求；
- 比赛时间；
- 官方通知；

判断赛事，并在进入正式流程前通过官方来源核对。识别有误时按 `WG-ROUTE-001` 执行影响追踪后再改判，不新建识别机制。

---

# 第三阶段：建立 Contest Profile

## 目标

真正把赛事差异从 Core 中剥离出来。三层职责（架构原则见“最重要的架构原则”第 7 条）：

- Core：通用工作流、数据复现、证据、sandbox、产物导航；
- Contest Profile：赛事规则、提交要求、赛事参数、统计口径、AI 披露方式、模板与样本映射；
- Project：当前项目采用哪个 profile，以及题目级决策。

建议建立：

```text
config/contests/
├── cumcm/
└── mcm-icm/
```

其中保存赛事专属规则、状态和配置。

结构可以类似：

```text
config/contests/cumcm/
├── profile.yaml
├── rules.md
├── paper.md
├── submission.md
└── ai.md
```

```text
config/contests/mcm-icm/
├── profile.yaml
├── rules.md
├── paper.md
├── submission.md
└── ai.md
```

实际文件是否完全按以上方式拆分，以“一个规则只定义一次”和可维护性为准，不要机械拆文件。

Profile 落位后必须同步处理：

- `docs/README.md` 的唯一权威职责矩阵新增“赛事 Profile”一行；
- 入口路由（`AGENTS.md`）按当前项目 profile 路由当届规则、提交格式与 AI 披露要求；
- profile 目录成为新的扫描根，引用完整性检查必须覆盖（见第九阶段）。

---

## 3.1 当前 CUMCM 专属内容

应进入 CUMCM Profile 的典型内容：

```text
CUMCM 页数限制
CUMCM 摘要专用页要求
CUMCM 支撑材料形式
CUMCM AI 声明具体格式
CUMCM AI 工具详情文件名
CUMCM 特定匿名要求
CUMCM 特定提交格式
CUMCM 特定论文结构
CUMCM 特定分页规则
CUMCM PDF 文件大小限制
CUMCM 当届官方规则
```

这些不能继续作为通用 Core 的硬规则。

---

## 3.2 MCM/ICM 专属内容

应进入 MCM/ICM Profile 的典型内容：

```text
MCM/ICM Summary Sheet
MCM/ICM solution 页数要求
COMAP 提交流程
MCM/ICM AI 使用报告
MCM/ICM 特定匿名规则
MCM/ICM 特定论文结构
MCM/ICM 文件要求
MCM/ICM 当届官方规则
```

---

## 3.3 不要把通用原则赛事化

例如：

```text
AI 使用应真实披露
AI 参与内容必须人工核验
外部资料必须引用
模型结果必须验证
论文结论必须来自真实结果
论文需要控制篇幅
交付材料需要匿名
```

这些属于通用原则。

但：

```text
CUMCM 使用某个声明
MCM 使用某个 Report on Use of AI
CUMCM 正文多少页
MCM solution 多少页
```

属于赛事实现。

正确结构：

```text
通用原则
    +
赛事特定规则
    ↓
当前项目要求
```

---

## 3.4 赛事规则的控制编号与引用

- profile 的官方规则基线使用带赛事标识的编号，例如 `OFFICIAL-CUMCM-001`、`OFFICIAL-MCM-001`；
- Core 文档、Skill 与模板不得直接引用具体赛事编号，改为引用中性锚点（当前项目赛事官方基线），由 profile 解析；
- 控制编号保持“每个被引用编号有且仅有一处权威定义”，该不变量由现有 smoke 测试机器强制；
- Core 文档中既有的赛事编号引用（`paper-writing.md`、`paper-formatting.md`、`workspace-governance.md` 等）在迁移阶段一并中性化。

---

# 第四阶段：Machine Contract 的 Profile 化

## 目标

本阶段不迁移赛事内容，只让契约加载支持 profile，并保证 CUMCM 行为逐键不变。

## 4.1 加载、作用域与优先级

`tools/control_contracts.py` 当前写死权威文档集合与 required keys，并被初始化器、审校脚本、影响追踪与测试共同使用，因此：

- 权威文档集合拆为 Core 文档集与 Profile 文档集两段加载；
- required keys 拆为 core-required 与 profile-required，闭集校验按段执行，profile 新增键不再触发“未知键”错误；
- 作用域：有项目上下文的调用按项目 profile 加载（初始化器由 `--contest` 解析，审校与影响追踪读项目配置）；无项目上下文的 workspace 级调用只加载 Core 契约，不设“默认赛事”；
- 优先级：Core 提供键名与结构，Profile 提供赛事取值与语义，Project 不覆盖契约键。

## 4.2 键的归属与文档的归属分离

- 键的归属不等于文档的归属：Core 权威文档保留门禁与键定义，取值由 profile 注入；
- 赛事官方数值（如 PDF 体积上限）随 profile 提供，不再写在 Core 文档里；
- 工作区内部下限（如竞争力页数、图表数量下限）保留在 Core；是否受赛事体系影响，按第一阶段盘点结论处理。

## 4.3 规则语义不能被数字统一

- 统一配置格式，不等于统一规则语义；
- 每个由 profile 提供的键必须能表达 `value`、`scope` 与 `counting rule`（统计口径），或显式声明语义单一无歧义；
- 明确案例：页数上限必须携带计页口径——CUMCM 为正文不含附录，MCM/ICM 为 solution 全文含 Summary Sheet，仅把 30 改为 25 是语义错误；
- 同类项至少包括字数下限、图表数量下限、文件体积上限与匿名范围，逐项判定。

## 4.4 完成判据

- 现有四个测试文件全绿；
- `load_workspace_contracts` 对 CUMCM 的返回值在 profile 化前后逐键 diff 为空；
- audit 脚本对同一 fixture 项目产出的 findings 不变。

以上成立后，才允许进入后续迁移阶段。

---

# 第五阶段：重构论文规范

当前论文规范中存在大量：

```text
通用数学建模论文原则
+
CUMCM 特定要求
```

需要拆开。

---

## 5.1 通用论文规范

例如下面这些可以保留在通用 `paper-writing.md`：

```text
题目理解
问题数学化
模型假设
变量与符号
模型建立
算法与求解
结果分析
模型验证
敏感性 / 稳健性分析
模型优缺点
模型推广
证据闭环
科学表达
引用真实性
AI 使用真实性
```

核心是：

> **如何写一篇高质量数学建模论文。**

---

## 5.2 赛事特定论文要求

下面内容放进赛事 Profile：

```text
摘要 / Summary 的具体格式
章节结构是否固定
页数与页数统计口径（如 CUMCM 正文不含附录、MCM/ICM 全文含 Summary Sheet）
分页方式
页边距
字体
字号
目录
附录
Summary Sheet
AI Report
submission PDF
submission package
```

不要把“论文存在共同结构”误解为“所有比赛使用同一个论文模板”。

---

# 第六阶段：重构 Samples / Templates

## 目标

当前工作区 Samples 以 CUMCM 为主，需要真正成为多赛事参考体系。

---

## 6.1 通用模板与赛事模板分离

当前：

```text
resources/templates/cumcm-paper-framework.tex
```

不再适合作为整个工作区唯一论文模板。

建议逐步改为：

```text
resources/templates/
├── common/
│   ├── artifact-map.yaml
│   └── figure-selection-record.md
│
└── contests/
    ├── cumcm/
    │   └── paper-framework.tex
    │
    └── mcm-icm/
        └── paper-framework.tex
```

实际目录设计以最终方案为准。

---

## 6.2 CUMCM LaTeX Sample

当前 CUMCM LaTeX 模板继续保留，作为：

> CUMCM 赛事模板 / Sample

需要检查：

- 是否仍与最新 CUMCM 规则一致；
- 哪些部分是通用论文结构；
- 哪些部分是 CUMCM 特定版式；
- 模板是否无意中成为隐性规则来源。

原则：

> 模板只实现规则，不重新定义规则。

---

## 6.3 新增 MCM/ICM LaTeX Sample

寻找一篇：

> **开源、可合法使用、质量较高、具有代表性的 MCM/ICM 优秀论文 LaTeX 源码。**

优先要求：

- 有完整 LaTeX source；
- 公开授权或明确允许使用；
- 论文结构完整；
- 数学建模表达质量较高；
- 能体现 MCM/ICM 常见论文组织方式；
- 具有较高学习价值。

处理方式：

```text
原始开源论文
    ↓
结构分析
    ↓
提取可迁移的论文组织方式
    ↓
识别 MCM/ICM 特有格式
    ↓
重新整理
    ↓
形成工作区 MCM/ICM Sample
```

不要直接把第三方优秀论文复制成模板。

应记录：

- 原作者；
- 原始项目；
- 原始链接；
- License；
- 取得日期；
- 使用范围；
- 学习内容；
- 明确禁止复制的内容。

---

## 6.4 Sample、Rule、Reference 三者分离

最终明确：

```text
Rules
= 官方赛事要求

Template
= 对规则的实现

Sample Paper
= 优秀论文学习与参考
```

不能互相替代。

例如：

```text
MCM 官方规则
    ↓
MCM/ICM Profile
    ↓
MCM/ICM LaTeX Template
```

优秀论文只用于：

```text
论文学习
结构参考
表达参考
图表参考
论证方式参考
```

不能成为赛事规则来源。

参考论文库按赛事打标：`learning_paper_minimum` 要求的样本必须来自当前项目赛事；跨赛事样本只能作表达参考，不能充当写作前学习门禁样本。

---

# 第七阶段：改造 Skills，不增加赛事 Skill

## 总原则

**尽量维持现有“两大 Skill”架构。**

当前：

```text
.codex/skills/
├── cumcm-paper-production/
└── cumcm-paper-audit/
```

最终优先改造成通用：

```text
.codex/skills/
├── modeling-paper-production/
└── modeling-paper-audit/
```

具体名称可以调整，但不要为了赛事扩展而不断增加 Skill。

---

## 7.1 Production Skill

Production Skill 不再写死 CUMCM。

执行逻辑：

```text
Project
    ↓
00-admin/project.yaml
    ↓
resolve contest profile
    ↓
读取通用 Core
    ↓
加载对应 Contest Profile
    ↓
执行通用数学建模生产流程
    ↓
应用赛事特定规则
```

只改名不算完成：必须验证 Skill 内不存在写死的赛事名称、规则、路径与编号；Skill 通过 profile 解析获取赛事规则，并引用中性锚点而非具体赛事编号（见 3.4）。

Skill 负责：

> 编排流程。

不负责：

> 重新定义赛事规则。

---

## 7.2 Audit Skill

Audit Skill 同样不再写死 CUMCM。

执行逻辑：

```text
读取 00-admin/project.yaml 并解析 profile
    ↓
加载通用审查要求
    ↓
加载对应赛事 Profile
    ↓
检查通用质量
    ↓
检查赛事特定要求
    ↓
形成审查结论
```

---

## 7.3 除非确有必要，不新增以下 Skill

不要轻易建立：

```text
cumcm-production
mcm-production
cumcm-audit
mcm-audit
contest-identification
contest-selection
contest-classification
```

不要用 Skill 数量解决本应由 Profile 解决的问题。

---

# 第八阶段：工具与初始化器通用化

## 8.1 初始化器

当前：

```text
init_cumcm_project.py
```

逐步改造成通用：

```text
init_modeling_project.py
```

调用形式类似：

```powershell
.\.venv-modeling\Scripts\python.exe `
  .codex\skills\modeling-paper-production\scripts\init_modeling_project.py `
  --root workspace\projects `
  --contest cumcm `
  --year 2027 `
  --problem a
```

或者：

```powershell
.\.venv-modeling\Scripts\python.exe `
  .codex\skills\modeling-paper-production\scripts\init_modeling_project.py `
  --root workspace\projects `
  --contest mcm-icm `
  --year 2027 `
  --problem a
```

初始化器根据赛事 profile：

```text
创建通用项目骨架
+
加载对应赛事模板
+
写入 00-admin/project.yaml 的 contest / profile
```

此时项目文件尚未生成，profile 只能从 `--contest` 解析；解析结果与后续读 `project.yaml` 的结果必须一致。

不要建立：

```text
init_cumcm_project.py
init_mcm_project.py
init_mathorcup_project.py
```

这样的复制结构。

---

## 8.2 通用工具继续保持通用

以下工具本身原则上属于 Core：

```text
check-modeling-env.py
check-workspace-layout.py
extract-spreadsheet.py
extract-pdf-pages.py
trace-artifact-impact.py
control_contracts.py
```

除非工具逻辑本身确实存在赛事差异，否则不要在工具里写死赛事。

契约作用域例外：初始化器在项目文件生成前只能从 `--contest` 解析 profile；按 `WG-ROUTE-001` 在项目内运行的 `tools/trace-artifact-impact.py` 按项目 profile 加载；workspace 级调用（无项目上下文）只加载 Core 契约。

---

# 第九阶段：测试与兼容性

这是这次重构非常重要的一部分。

## 9.1 CUMCM 回归测试

必须证明：

```text
新通用 Core
+
CUMCM Profile
```

仍然可以实现当前成熟的 CUMCM 流程。

行为一致的客观判据：

```text
load_workspace_contracts 对 CUMCM 的返回值逐键 diff 为空
现有四个测试文件全绿
audit 脚本对同一 fixture 项目的 findings 不变
```

至少验证：

```text
新题进入 inbox
    ↓
识别 CUMCM
    ↓
写入 project.yaml（contest / profile）
    ↓
初始化
    ↓
数据处理
    ↓
模型选择
    ↓
模型 / 代码
    ↓
正式结果
    ↓
证据
    ↓
论文
    ↓
Audit
    ↓
Delivery
```

现有 CUMCM 能力不得因为通用化而退化。

---

## 9.2 MCM/ICM Smoke Test

先用一个简单 MCM/ICM 示例验证：

```text
inbox
    ↓
Agent 判断 MCM/ICM
    ↓
project.yaml（contest / profile）
    ↓
加载 MCM/ICM Profile
    ↓
使用 MCM/ICM Template
    ↓
通用 Production
    ↓
通用 Audit
    ↓
正确执行 MCM/ICM 特有要求
```

第一阶段不要求把所有 MCM/ICM 细节一次做完。

重点是证明：

> **同一个通用系统可以正确切换赛事规则。**

---

## 9.3 全仓硬编码检查

重构完成后全仓搜索：

```text
CUMCM
cumcm
MCM
ICM
COMAP
```

重点检查是否存在：

- 通用规范仍写死 CUMCM；
- Skill 仍写死 CUMCM；
- 初始化器仍只支持 CUMCM；
- README 仍把整个工作区定义成 CUMCM-only；
- 工具路径仍绑定 CUMCM；
- Template 被误当成规则；
- 赛事规则重复定义；
- 同一个规则在多个文件中出现不同版本。

检查方式：扩展既有 `tools/tests/test_v2_smoke.py`（控制编号唯一权威不变量与全链路 smoke）与 `tools/tests/test_audit_refactor.py`（契约加载器测试），不新增常驻检查脚本；扫描根扩展到 profile 目录。prose 层的赛事残留清单作为一次性盘点产物，不常驻自动化。

---

# 第十阶段：保持现有基础设施不被破坏

本次重构必须保持近期已经完成的基础设施成果。

不得破坏：

- Python 依赖精简后的 85 项锁定；
- Python 3.12–3.14 支持；
- UTF-8 stdout/stderr；
- UTF-8 文件读写；
- PDF 文本层 UTF-8；
- artifact-map；
- artifact impact tracing；
- sandbox；
- 工具测试；
- smoke test；
- 原始数据保护；
- 证据链；
- 单一权威原则；
- 按需加载规范。

不要为了增加赛事支持重新引入已经删除的、没有真实流水线需求的第三方依赖。

---

# 最终目标架构

```text
mathematical-modeling-workspace
│
├── config/
│   └── contests/
│       ├── cumcm/
│       └── mcm-icm/
│
├── docs/
│   ├── 通用工作区治理
│   ├── 数据与复现
│   ├── 建模与计算
│   ├── 证据
│   ├── 通用论文写作
│   ├── 通用图片规范
│   └── 通用审校
│
├── resources/
│   ├── algorithm-library/
│   ├── paper-library/
│   ├── figure-style-library/
│   └── templates/
│       ├── common/
│       └── contests/
│           ├── cumcm/
│           └── mcm-icm/
│
├── .codex/
│   └── skills/
│       ├── modeling-paper-production/
│       └── modeling-paper-audit/
│
└── workspace/
    ├── inbox/
    ├── projects/
    │   └── <project-id>/
    │       └── 00-admin/
    │           └── project.yaml（含 contest / profile）
    └── archive/
```

---

# 最终运行逻辑

```text
新赛题进入 inbox
        ↓
Agent 阅读题面与附件
        ↓
判断所属赛事
        ↓
官方来源核验
        ↓
创建项目
        ↓
写入 00-admin/project.yaml（contest / profile）
        ↓
加载通用 Core
        +
加载对应 Contest Profile
        ↓
通用 Production Skill
        ↓
赛事特定规则 / Template / Submission
        ↓
通用 Audit Skill
        ↓
赛事特定 Audit
        ↓
Delivery
```

---

# 最重要的架构原则

## 1. 流程通用化

不要：

```text
CUMCM 一套完整流程
MCM 一套完整流程
```

而要：

```text
一套通用数学建模生产流程
+
不同赛事规则
```

## 2. 规则配置化

赛事规则进入：

```text
Contest Profile
```

而不是复制一套 Skill。

## 3. Sample / Template 赛事化

论文模板允许不同赛事拥有不同实现：

```text
CUMCM Template
MCM/ICM Template
```

但通用论文原则仍然只有一套。

## 4. Skill 不按赛事复制

优先保持：

```text
modeling-paper-production
modeling-paper-audit
```

两个核心 Skill。

## 5. Agent 负责识别赛事

不增加专门赛事识别 Skill。

```text
inbox
→ Agent 判断
→ 官方核验
→ project.yaml（contest / profile）
→ 正式流程
```

## 6. 通用化不是强行统一

目标不是：

> 让 CUMCM 与 MCM/ICM 使用相同的论文格式。

目标是：

> 让 CUMCM、MCM/ICM 使用同一套数学建模生产基础设施，并通过赛事 Profile 正确处理各自差异。

统一配置格式不等于统一规则语义；规则语义不能被数字统一（执行要求见 4.3）。

## 7. 三层职责

```text
Core / Workspace Authority
        ↓
Contest Profile
        ↓
Project
```

Profile 是赛事规则域的唯一权威，不是新的全局规则中心；项目只引用 profile，不重复定义赛事规则。

## 8. 机器层先行

```text
机器层先具备多赛事能力，再搬迁赛事规则；
先保证 CUMCM 不退化，再接入 MCM/ICM。
```

---

# 推荐实施顺序

```text
Phase 1
全仓 CUMCM 耦合审计 + 语义级分类（含 machine contract 键）
        ↓
Phase 2
边界冻结：Core / Workspace Default / Contest Profile / Contest-shaped heuristic / Project-local
        ↓
Phase 3
机制设计冻结：Profile Schema、project.yaml、契约加载与优先级、控制编号策略
        ↓
Phase 4
control_contracts.py Profile 化（CUMCM 行为逐键不变）
        ↓
Phase 5
建立 CUMCM Profile，验证行为一致
        ↓
Phase 6
迁移 CUMCM 规则、模板与引用（同步扩展引用完整性扫描根）
        ↓
Phase 7
CUMCM 回归
        ↓
Phase 8
MCM/ICM Profile + Contract（验证 profile 抽象是否充分）
        ↓
Phase 9
MCM/ICM Samples / Templates（开源许可核查前置）
        ↓
Phase 10
Skill / initializer / 入口通用化
        ↓
Phase 11
最终去重 + smoke test
```

**核心顺序：机器层先具备多赛事能力，再搬迁赛事规则；先保证 CUMCM 不退化，再接入 MCM/ICM。**

**Phase 1 只做盘点和拆分设计，不直接进行大规模文件迁移。**

只有在明确：

```text
哪些属于 Core / Workspace Default
哪些属于 Profile
哪些属于 Contest-shaped heuristic / Project-local
```

之后，再正式开始结构重构。
