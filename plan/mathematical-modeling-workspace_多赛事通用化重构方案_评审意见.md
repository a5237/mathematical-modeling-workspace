# 多赛事通用化重构方案 · 评审意见

> 评审对象：`plan/mathematical-modeling-workspace_多赛事通用化重构方案.md`
>
> 评审依据：当前仓库实际文件、控制编号、机器契约与测试覆盖
>
> 结论：方向与原则成立，可作为重构纲领；但方案只覆盖文档层，未覆盖承载赛事差异的机器契约层与既有不变量，Phase 4 依原顺序执行会中途破坏基础设施。

---

## 一、与现状核对后的事实

### 1.1 硬耦合只有 5 处，规模被高估

- `docs/standards/cumcm-current-rules.md`：唯一赛事专属文档（`OFFICIAL-CUMCM-001`，含官方链接、年度快照、AI 规则生效边界）。
- 控制编号引用：`paper-writing.md` 13 处（其中 10 处为 `OFFICIAL-CUMCM-001` 引用）、`workspace-governance.md`、`paper-formatting.md:9,159`、`AGENTS.md:24`、`docs/README.md:22`、`init_cumcm_project.py`、`audit_cumcm_project.py:366`。
- `resources/templates/cumcm-paper-framework.tex`，路径写死在 `docs/standards/naming.md:28`。
- Skill 与脚本命名：`.codex/skills/cumcm-paper-production/`、`cumcm-paper-audit/`、`init_cumcm_project.py`、`audit_cumcm_project.py`。
- 入口叙事：`README.md:41,72,75,77,149,286`、`docs/guides/paper-production.md:10,18,24`。

已属纯 Core 的部分（无需拆分）：`paper-quality-audit.md`、`workspace-layout.md`、`modeling-execution.md`、`data-reproducibility.md`、`paper-figures.md`、`tools/check-workspace-layout.py` 均为 0 处赛事字样；`paper-formatting.md` 仅 2 处，且均为"服从 `OFFICIAL-CUMCM-001`"。预期 Phase 1 矩阵结果为约 80% CORE。真正工作量在 1.3。

### 1.2 初始化器已半通用

- `init_cumcm_project.py:191,201` 已接受 `--contest`（默认 `cumcm`）。
- `init_cumcm_project.py:206` 已按 `<contest>-<year>-<problem>` 生成项目 ID，与 `naming.md:7` 一致。
- `init_cumcm_project.py:22` 已在 `00-admin/project.yaml` 写入 `contest:` 字段。
- `tools/tests/test_v2_smoke.py:118` 已用 `--contest smoke` 跑通过全链路。

因此方案 7.1 的实际内容是"改名 + 按 profile 选模板 + 校验 profile"，不是重写。

### 1.3 机器契约层未进入方案（最大缺口）

- `tools/control_contracts.py:20-30` 的 `DOCUMENTS` 写死 9 个权威文件；`:37-84` 的 `REQUIRED_KEYS` 写死 51 个键。
- 赛事数值藏在权威文档的 `toml machine-contract` 块内：`docs/standards/cumcm-current-rules.md:9-11`（`paper_maximum_bytes = 20000000`）。
- 契约消费方 4 处：`init_cumcm_project.py:197`、`audit_cumcm_project.py:295`、`tools/trace-artifact-impact.py:29`、`tools/tests/test_audit_refactor.py:65,77,163` 与 `tools/tests/test_v2_smoke.py:98`。
- 数值同时散落在 Core：`docs/standards/paper-quality-audit.md:8-9`（`body_page_minimum = 20`、`body_page_maximum = 30`）、`docs/standards/paper-writing.md:10`（`body_word_minimum = 5000`）等。

两点推论：

1. 把 CUMCM 规则搬进 profile 之前，必须先让 `control_contracts.py` 支持 core + profile 两段契约；否则 Phase 4 一动文件，初始化器与审校脚本同时失效，违反方案自身的 Phase 9。
2. Core 契约键混合了两类语义：官方上限（赛事）与工作区竞争力下限（通用）。Phase 2 的分类必须下探到每个契约键，而非只分文档。

### 1.4 计页口径是隐藏陷阱

CUMCM 30 页指正文不含附录；MCM 25 页指 solution 全文含 summary sheet。仅把 `body_page_maximum` 参数化为 25 是语义错误，契约需同时表达"口径"。这是"不为统一而抹平差异"在机器层的落点。

### 1.5 Phase 8.3 / Phase 9 与既有机制重叠

`tools/tests/test_v2_smoke.py:57-108` 已机器强制"每个被引用的控制编号有且仅有一处权威定义"，`specification_files()`（`:64-77`）扫描 `AGENTS.md`、`README.md`、`docs/`、`.codex/skills/`、`resources/templates/`。

- Core 文档需要一种赛事无关的控制编号引用方式，否则 Core 永远写死 CUMCM。
- Profile 若落在 `config/contests/`，必须扩展扫描根，否则断言直接失败。
- 按最小机制原则，8.3 与 Phase 9 应扩展现有 smoke 测试，而非新增常驻检查脚本；prose 层残留清单可作一次性盘点产物。

### 1.6 `contest.yaml` 与 `project.yaml` 重复

`00-admin/project.yaml` 已含 `contest/year/problem/status/random_seed`，方案拟在同一目录新增 `contest.yaml`，形成双赛事身份源，与"每项规则只定义一次"冲突。二者需合并或明确迁移，不应并存。

---

## 二、方案中应当保留的部分

- 5.4 的 Rules / Template / Sample 三者分离，以及"模板只实现规则，不重新定义规则"，命中现有风险（模板路径被写入命名规范、模板注释可能被当规则引用）。
- 6.3、7.1 明确禁止按赛事复制 Skill 与初始化器，抑制最常见的退化形式。
- 原则 5、6、7（Agent 识别赛事、不强行统一、官方规则 > 工作区默认）与仓库既有的单一权威、官方基线机制一致。
- Phase 8 先证 CUMCM 不退化再谈 MCM，且 MCM 仅要求 smoke、不要求一次做全，边界合理。

---

## 三、待定设计决策

| 决策 | 倾向 |
|---|---|
| `contest.yaml` 独立 vs 扩展 `project.yaml` | 扩展 `project.yaml`，避免双身份源 |
| profile 是否构成第二权威根 | 是则 `docs/README.md` 权威矩阵必须加行；注意 `config/` 现语义为环境/依赖配置 |
| workspace 级契约加载（`test_v2_smoke.py`、`trace-artifact-impact.py` 无项目上下文）用哪套数值 | core-only + 项目级覆盖，不设默认赛事 |
| 赛事识别留痕与核验证据归属 | 挂 `WG-EVID-001`，不新建台账 |
| AI 披露的切分点 | 精确到"谁规定格式、谁规定存放位置"：CUMCM 为正文声明 + 支撑材料独立 PDF，MCM 为 Report on Use of AI，否则 `WG-AI-001` 冲突 |
| 识别错赛事的改判路径 | 挂 `WG-ROUTE-001` 影响追踪，不新建机制 |
| `paper-library` 是否按赛事打标 | 若 MCM 学习需 MCM 样本则必须打标，方案目标架构未涉及 |
| Phase 5.3 开源 MCM 论文许可 | 许可核查作为该阶段门禁，而非事后补记 |

---

## 四、建议阶段顺序

1. Phase 1 盘点 —— 保留，范围下探到每个 machine-contract 键。
2. Phase 2 分类 —— 增加"契约键归类"：官方上限 / 工作区下限 / 计页口径。
3. Phase 3 设计冻结 —— `contest.yaml`、profile 位置、控制编号策略、契约加载作用域四项一次定完，先不改文件。
4. **新增：`control_contracts.py` profile 化** —— 保持 CUMCM 行为不变，回归全绿。
5. CUMCM 规则与模板迁入 profile，同时扩展 smoke 扫描根 —— 回归仍全绿。
6. Skill 更名与 `OFFICIAL-CUMCM-001` 引用中性化。
7. MCM profile 与 MCM sample（许可核查前置）。
8. CUMCM 回归 + MCM smoke。
9. 入口文档更新与规则去重 —— 由既有 smoke 测试承载。

与原顺序的唯一差别：先让机器层支持 profile，再搬文件。

---

# 五、对“局部修订说明（9 条）”的评价

评价对象：基于第一轮评审生成、用于修订原方案的 9 条要求。

结论：方向正确，9 条中 6 条与第一轮评审一致，2 条为有效增补；存在 3 处内部矛盾与 4 处仍缺环节，已在原方案本次修订中一并处理。

### 5.1 有效增补

- `Contest-shaped heuristic` 档位是真新增价值，命中项可点名：`body_page_minimum = 20`（相对 CUMCM 30 页体系的竞争力下限）、`body_word_minimum = 5000`（中文写作口径）、`learning_paper_minimum = 2`（`docs/guides/pre-writing-learning.md:6`，样本须来自同赛事论文库，而现库为 CUMCM）。
- 三层职责与仓库既有的“官方底线 / 工作区增补”区分同构（`docs/standards/cumcm-current-rules.md:25`），落地阻力小。
- “Profile 是赛事规则域的唯一权威，不是新的全局规则中心”是本轮最重要的护栏。
- 修订说明只给问题不给答案，与“设计冻结”阶段配合成立。

### 5.2 内部矛盾

1. 两套分类并存且无映射：`MIXED` 的产出无法判读归属。
2. 规则语义要求只覆盖页数：字数下限、图表下限、体积上限、匿名范围同属一类。
3. 保留清单漏掉原 Phase 9（基础设施不得破坏），而它正是本次重排的理由。

### 5.3 仍缺环节

1. 控制编号策略无归属：`OFFICIAL-CUMCM-001` 在 Core 文档 13 处、Skill 与脚本 4 处；`tools/tests/test_v2_smoke.py:57-108` 机器强制唯一权威定义，`specification_files():64-77` 的扫描根不含 profile 新根。
2. `REQUIRED_KEYS` 闭合校验会拒绝 profile 键（`tools/control_contracts.py:111-119`）；需拆分并明确“键归属 ≠ 文档归属”。
3. 测试落点写错：契约加载器测试在 `tools/tests/test_audit_refactor.py:61-83`，不在 smoke 文件。
4. “行为一致”缺客观判据；另有两处作用域事实需一并定：`tools/trace-artifact-impact.py:29` 与 `tools/tests/test_v2_smoke.py:98` 为 workspace 级加载，`init_cumcm_project.py:197` 先加载契约后写项目文件。

### 5.4 顺序优化

MCM/ICM Profile + Contract 与 MCM/ICM LaTeX Sample 解耦：前者是架构验证，应尽早；后者依赖开源许可核查，属慢任务。

### 5.5 本次修订落地对照

| 修订要求 | 落地位置 |
|---|---|
| 语义级五档分类，契约键纳入盘点 | 1.1、1.3 |
| Machine Contract 阶段 | 新增第四阶段 |
| 三层职责与 Profile 权威边界 | 第三阶段、架构原则第 7 条 |
| 规则语义不能被数字统一 | 4.3、架构原则第 6 条 |
| `project.yaml` 扩展，删除 `contest.yaml` 身份源 | 2.1、2.2、目标架构、运行逻辑 |
| Skill 解析链与“只改名不算完成” | 7.1、7.2 |
| 控制编号策略 | 3.4 |
| 测试策略与客观判据 | 9.1、9.3 |
| 阶段顺序与 MCM 两阶段拆分 | 推荐实施顺序 |
| 基础设施不得破坏 | 第十阶段（保留） |

原第三节中“`contest.yaml` 双身份源”“Profile 权威边界”两项已定；profile 目录位置沿用原方案的 `config/contests/`，其权威矩阵与扫描根后果已写入第三阶段。第四节建议顺序已由修订后的“推荐实施顺序”取代。
