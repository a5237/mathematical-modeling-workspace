# 工作区全局治理规范

> 适用范围：跨阶段优先级、文件路由、权威来源、项目生命周期、证据与 AI 记录路由、生产—审校交接和交付治理。
>
> 不适用范围：数据与复现细则由 `docs/standards/data-reproducibility.md` 管理；模型、正式计算与验证由 `docs/standards/modeling-execution.md` 管理；论文内容、排版和图片分别由对应论文规范管理。
>
> 核心原则：**论文保持学术表达，工程信息留在工作区；所有结果可运行、可定位、可核验、可交付。门禁用于防止步骤遗漏，不用于冻结合理迭代。**

本文只定义跨阶段治理。各主题的唯一权威见 `docs/README.md`；本文引用其它控制项时不重述其阈值、字段或判断标准。

```toml machine-contract
artifact_path_categories = ["data", "code", "parameters", "results", "validation", "paper_assets"]
artifact_semantic_categories = ["evidence", "paper", "review", "delivery"]
artifact_index_names = ["problem", "runbook", "model_selection", "claims", "literature", "paper", "review", "delivery"]
artifact_question_evidence_fields = ["claim_ids", "citation_keys"]
problem_attachment_columns = ["relative_file", "exists", "source", "received_at"]
problem_question_columns = ["question_id", "task", "inputs", "outputs", "constraints", "metric", "depends_on", "required_deliverables", "status"]
problem_risk_columns = ["data_gaps", "external_sources", "provisional_assumptions", "rules_checked_at"]
ai_log_columns = ["date", "tool_and_model", "stage", "material_prompt_or_method", "adopted_content", "human_changes", "verification"]

[artifact_index_categories]
claims = "evidence"
literature = "evidence"
paper = "paper"
review = "review"
delivery = "delivery"

[artifact_impact_defaults.results]
depends_on = ["data", "code", "parameters"]
effect = "STALE"

[artifact_impact_defaults.validation]
depends_on = ["results"]
effect = "STALE"

[artifact_impact_defaults.paper_assets]
depends_on = ["results"]
effect = "STALE"

[artifact_impact_defaults.evidence]
depends_on = ["results", "validation"]
effect = "RECHECK"

[artifact_impact_defaults.paper]
depends_on = ["results", "validation", "paper_assets", "evidence"]
effect = "RECHECK"

[artifact_impact_defaults.review]
depends_on = ["paper", "evidence"]
effect = "RECHECK"

[artifact_impact_defaults.delivery]
depends_on = ["paper", "review"]
effect = "RECHECK"
```

上方字段是初始化器、影响追踪器和客观检查使用的稳定接口。模板只实现这些字段，不拥有其语义或默认依赖。

---

## 1. 优先级与按需加载

发生冲突时按以下顺序执行：

1. 比赛当届官方规则与用户当前明确要求；
2. 本工作区各主题的唯一权威规范；
3. 项目内 `00-admin/` 的明确约定；
4. 工具默认行为。

Agent 先按 `AGENTS.md` 分类任务，只加载直接相关的权威文件。普通局部任务不得因为位于本工作区而自动升级为完整生产流程、完整审校或全部规范预读。

工作区必须保存复现所需的工程信息，但不得自动把环境、命令、路径、日志、证据索引、AI 台账或审校过程写入正文；只有评审理解模型和结论必需的科学设置才进入论文。

各权威文件统一使用以下规范词：**必须 / 不得**表示发布硬要求；**应 / 原则上**表示默认要求，题型不适用时须采用等效措施并说明；**宜 / 推荐**表示质量建议；**可**表示允许。控制编号不自动等于机器 hard gate，机器边界仍按第 4 节执行。

---

## 2. 文件路由与权威来源（`WG-ROUTE-001`）

仓库级和项目级文件按 `docs/architecture/workspace-layout.md` 路由，稳定命名按 `docs/standards/naming.md` 执行。普通目录组织、文件命名、根目录整洁和 `q01` 等稳定标识属于 Agent 工程责任；只有路径错误会破坏运行、解析、追溯或正式提交时才由机器阻断。

以下约束不可绕过：

- 原始数据执行 `docs/standards/data-reproducibility.md` 的 `WG-DATA-001`；
- 主张和文献证据执行 `docs/standards/evidence-contract.md` 的 `WG-EVID-001`；
- 临时产物不得成为唯一证据或交付物；
- 同一数据、参数、指标、图表和论文不得维护多个相互竞争的“最终版”。

原始数据、机器结果、论文主源和发布文件分别以项目目录树中登记的对应产物为权威。具体位置执行工作区架构，版本命名执行命名规范。

`00-admin/artifact-map.yaml` 是跨阶段快速导航入口，不是新的权威来源、完整 manifest、证据台账或阶段门禁。它由 `indexes`、`common` 和稳定 `question_id` 条目组成；`common` 与各问只登记上方 `artifact_path_categories` 中下游会复用的稳定关键路径，证据条目只登记 `claim_id` 和 `citation_key`。路径相对项目根目录，`paper_assets` 只指向 `06-paper/figures/` 或 `06-paper/tables/` 的实际引用副本。不得登记临时文件、缓存、失败输出、全部辅助代码、哈希、存在状态、阶段完成状态或 `sandbox/` 产物。

进入论文写作、结果分析、制图或审校时，先读取 `common` 和当前子问题条目，再到运行手册、模型记录与证据台账核验语义和状态。创建、移动或淘汰会被下游复用的稳定关键文件时更新对应条目；旧项目缺失地图或条目失效时，只在相关职责目录定向搜索并修复本次实际使用的路径，不扩张为全项目补录，也不形成发布阻断。

通用影响关系只由上方 `artifact_impact_defaults` 定义，不复制进项目地图。只有本问结果实际依赖另一问的产物时，才在 `depends_on_questions` 登记 `<question_id>.<category>`。上游稳定产物发生实质变化后，向 `tools/trace-artifact-impact.py` 显式传入变化路径：`STALE` 产物必须重新生成，`RECHECK` 内容结合新结果核对后决定是否更新。工具不读取 Git diff、不回写状态，其输出只是影响分析起点；实际 Final 复查范围执行 `docs/standards/paper-quality-audit.md`。

---

## 3. 项目初始化与问题清单

新需求先进入 `workspace/inbox/`，保存题目要求、用户说明和原始附件。明确比赛、年份和题号后，优先使用 Production Skill 初始化器在 `workspace/projects/` 创建推荐骨架；把题面与附件分类到 `01-problem/` 和 `02-data/raw/`，验证项目副本后再清空对应 inbox。

初始化骨架是可靠默认值，不是审计 schema。编号阶段旁的 `sandbox/` 保留为跨阶段实验沙盒；项目仍可按题目增加、拆分或重构 `benchmarks/`、`simulations/` 等其它目录，只要权威数据、模型、结果、证据和交付关系仍清楚且可复现。

建模前，`01-problem/problem-checklist.md` 至少记录：

- 题目版本，以及附件的相对文件名和存在状态；
- 每个子问题的输入、输出、约束和评价口径；
- 各问依赖关系与必须生成的论文或附件结果；
- 数据缺口、外部资料需求和暂定假设；
- 官方格式、AI 使用、匿名性和提交要求的核对日期。

需求变化时更新清单，不以聊天记忆或临时笔记作为唯一依据。项目还须按各自权威规则维护 `03-models/model-selection.md` 和 `00-admin/pre-writing-learning.md`。

---

## 4. 正式与实验产物边界（`WG-TEST-001`）及轻量迭代

- `sandbox/` 是编号阶段之外的可选实验沙盒，不形成新阶段、完成状态或门禁。其代码、数据、参数、输出和记录一律为 exploratory 非权威产物，不进入产物地图、证据台账、论文引用或交付。
- 实验只用于决策。采纳方案必须在适用编号阶段重新实现，以正式数据运行并完成对应验证和证据登记；随后只以实际变化的正式路径触发影响分析。未采纳实验和单纯 `sandbox/` 变化不进入正式影响链。
- `sandbox/` 不得替代或降低数据、模型、复现、验证、证据、写作、图片或发布控制项；实验设计与采纳判据执行 `WG-MODEL-001`，实验数据保护执行 `WG-DATA-001`。
- 开发与中间阶段只登记关键产物的相对文件名、存在状态和阶段完成状态，不绑定代码、数据、模型、参数、图片或表格的内容哈希。
- 阶段通过只表示必要步骤和产物没有遗漏，不冻结文件内容。发现问题时返回受影响阶段，只更新相关产物、验证和状态。
- 自动检查只核对稳定、客观的存在性与状态字段；内容是否充分、模型是否适用和论证是否可信仍由 Agent 与独立 Reviewer 根据权威证据判断。
- 控制编号不自动等于机器 hard gate。机器只阻断高风险、客观、稳定且可自动判断的问题；普通路由、命名、模型适用性、论证和视觉质量由 Agent 或独立 Reviewer 判断。
- Final Audit 的 PDF 哈希、失效与复查范围只执行 `docs/standards/paper-quality-audit.md`。

完整生产流程由 `.codex/skills/cumcm-paper-production/SKILL.md` 编排；完整最终审校由 `.codex/skills/cumcm-paper-audit/SKILL.md` 编排。Skill 只执行权威规则，不建立第二套门禁。

---

## 5. 证据与 AI 使用生命周期

所有重要数值和事实主张必须按 `WG-EVID-001` 登记，并在写入论文前达到证据契约要求的状态。文献检索与核验记录也执行 `docs/standards/evidence-contract.md`；论文中的文献组成和引用表达执行 `docs/standards/paper-writing.md`。

### 5.1 AI 使用台账（`WG-AI-001`）

`05-evidence/ai-tool-log.md` 按“实质影响事件”登记：

- 主要 AI 工具、模型或版本、机构和日期；
- 主要使用阶段与目的；
- 对模型、代码、论文或交付有实质影响的典型提示方式或方法；
- 主要采纳内容及其对应位置；
- 人工修改、验证方式与证据。

普通问答、每个小 prompt、措辞微调、无实质影响的交互和完整聊天流水账不必记录。按 `docs/standards/cumcm-current-rules.md` 从台账生成当届要求的声明和详情文件，不得在比赛结束时凭记忆补写 material AI usage。

---

## 6. 生产、审校与发布（`WG-RELEASE-001`）

`06-paper/figures/` 与 `06-paper/tables/` 只保存论文实际引用的副本，并能追溯到 `04-results/` 的权威产物。论文中人工复制的数值必须与机器可读来源进行自动或人工双重核对，全部图片必须通过 `PW-FIG-001`。

生产阶段负责从权威数据、代码、结果、证据和论文源持续生成可检查产物，不维护 final hash 或持续有效的发布结论。形成待审快照后交给独立 Final Audit；完整审查步骤、Draft/RC/Final 生命周期、复查范围、报告字段和发布判定只执行 `docs/standards/paper-quality-audit.md`。审查发现问题必须回到权威数据、代码或论文源修复，不得在 `07-review/` 静默修改成品。

### 6.1 交付包

`08-delivery/` 只保留 `OFFICIAL-CUMCM-001` 与赛题实际要求提交的成品和 `file-list.md`；目录路由与临时文件卫生执行工作区架构和数据复现规范，匿名性与正文/附录一致性执行论文写作规范。具体交付内容由当届官方要求决定，并统一纳入 `PQA-RELEASE-001`，本节不复制提交清单。

---

## 7. 全局发布检查表

- [ ] 文件路由与单一权威来源符合 `WG-ROUTE-001`。
- [ ] `WG-DATA-001`、`WG-MODEL-001`、`WG-EVID-001`、`PWL-GATE-001` 及适用的论文门禁已有权威证据。
- [ ] 正式运行、稳定产物和复现记录符合数据与复现规范，论文引用副本与权威结果一致。
- [ ] Final Audit 已完成 `WG-RELEASE-001`、`PW-FIG-001` 和 `PQA-RELEASE-001`。
- [ ] 交付目录符合本规范第 6.1 节及当届官方要求。
