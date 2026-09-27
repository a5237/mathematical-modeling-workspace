# 论文最终审查与竞争力评分标准

> 适用范围：Release Candidate（RC）与 Final 阶段的独立审查、发布判定和获奖竞争力评估。
>
> 核心原则：**最终审查只执行一次完整验证；客观硬错误决定能否发布，竞争力评分只用于判断质量和指导修改。**

```toml machine-contract
release_core_files = [
  "00-admin/runbook.md",
  "00-admin/pre-writing-learning.md",
  "00-admin/figure-selection-record.md",
  "01-problem/problem-checklist.md",
  "02-data/data-audit.md",
  "03-models/model-selection.md",
  "05-evidence/evidence-index.csv",
  "05-evidence/literature-ledger.csv",
  "05-evidence/ai-tool-log.md",
  "06-paper/main.tex",
  "07-review/review-log.md",
]
review_log_columns = ["id", "severity", "location", "criterion", "finding", "evidence", "required_fix", "verification", "status"]
review_open_statuses = ["OPEN", "BLOCKED"]
final_audit_fields = [
  "audit_date",
  "audit_phase",
  "review_scope",
  "final_pdf",
  "final_pdf_sha256",
  "official_rules_gate",
  "evidence_gate",
  "clean_reproduction_gate",
  "anonymity_gate",
  "delivery_gate",
  "open_critical",
  "open_major",
  "release_decision",
]
final_audit_pass_fields = ["official_rules_gate", "evidence_gate", "anonymity_gate", "delivery_gate"]
final_audit_zero_fields = ["open_critical", "open_major"]
release_candidate_phase_value = "RELEASE_CANDIDATE"
final_phase_value = "FINAL"
release_candidate_review_scopes = ["FULL"]
final_review_scopes = ["FULL", "IMPACTED"]
release_candidate_reproduction_statuses = ["PASS"]
final_reproduction_statuses = ["PASS", "REUSED_UNCHANGED"]
final_audit_pass_status = "PASS"
final_audit_no_open_findings_value = "0"
release_ready_status = "READY"
body_figure_minimum = 5
body_table_minimum = 2
```

上方字段承载本工作区明确保留的客观篇幅/图表门禁、审查交接文件、报告字段及状态枚举；竞争力评分不属于机器契约。`body_figure_minimum` 与 `body_table_minimum` 是全赛事通用的编号图、编号表下限，其统计区段仍由当前项目赛事 profile 定义。

---

## 1. 唯一最终审查

生产阶段负责正确生成和维护数据、代码、结果、证据、论文与交付材料，不维护最终 PDF 哈希或持续有效的发布结论。独立 Final Audit 在 RC 阶段接管并形成唯一报告：

`07-review/final-audit.md`

该报告合并原发布合规审查与论文质量审查。不得再维护互相竞争的 `release-audit.md` 和 `paper-quality-audit.md` 两套结论；旧项目可在下一次实质修改前继续保留历史文件，新审查统一写入 `final-audit.md`。

最终审查同时依据：

1. 已重新核验的当届官方规则与赛题要求；
2. `docs/standards/data-reproducibility.md`、`docs/standards/modeling-execution.md` 和 `docs/standards/evidence-contract.md`；
3. `docs/standards/paper-writing.md`、`docs/standards/paper-formatting.md` 和 `docs/standards/paper-figures.md`；
4. 题面、权威数据、代码、参数、结果和证据索引；
5. 本标准的硬错误边界和竞争力评分口径。

作者自述、聊天记录、未保存输出或旧审查结论均不能替代证据。

## 2. 生命周期与复查范围

### 2.1 Draft

Draft 的中间状态与哈希治理执行 `docs/standards/workspace-governance.md` 第 4 节。审查侧不要求完整审查持续有效；静态工具可给出提示，但除适用权威文件已定义的即时高风险问题外，不以项目尚未完成为由阻断草稿工作。

### 2.2 Release Candidate

将当前主要代码、数据处理、参数、证据和论文内容标记为待审快照后：

1. 在 clean directory 或等效干净环境中完整执行正式入口一次；
2. 核对关键指标、表格、图片与证据；
3. 生成拟交付 PDF；
4. 对该 PDF 执行一次完整的逐页、逐图、匿名性和交付检查；
5. 保存最终 PDF 哈希及 `final-audit.md`。

这次更强的 clean reproduction 同时满足生产交接与最终审查，不得在此前机械增加一次完全相同的全量重跑。

RC 不是不可逆冻结。若审查发现代码、模型、数据处理或论文仍需修正，应返回相应上游阶段，更新受影响产物、验证和完成状态，再形成新的 RC；未受影响阶段无需因文件内容变化机械重做。

### 2.3 Final

修改后按影响范围复查：

| 修改类型 | 必须重新验证 |
|---|---|
| 错别字或不影响分页的局部措辞 | 更新 PDF 哈希，复查受影响页面及相邻断行 |
| 局部排版但分页未变化 | 复查受影响页面、相邻页面和对应图表 |
| 图片、图题、表格或分页变化 | 复查受影响图表、页面及引用一致性；分页全局变化时重看全部页面 |
| 数据、代码、模型、参数或结果生成逻辑变化 | 重跑受影响计算；会改变全局产物时重新 clean reproduction |
| 官方规则、匿名性或交付内容变化 | 重跑相应合规与交付检查 |

最终 PDF 发生任何变化都要更新哈希，但不等于必须重跑模型或重做全部图片审查。`review_scope` 使用 `FULL` 或 `IMPACTED`，后者必须在报告中列出变化、影响分析和实际复查范围。

## 3. 机器与 Reviewer 的边界

### 3.1 机器可阻断事项

机器检查优先用于高风险、客观、稳定且低成本的事项：

- 核心交付文件或最终审查报告缺失；
- PDF 大小、篇幅、页数、图数和表数违反明确阈值；
- 最终 PDF 哈希与审查对象不一致；
- 证据字段无效、权威产物缺失或路径逃逸；
- 模型选择与写作前学习的稳定状态字段失败；
- 官方规则、匿名性、clean reproduction、证据或交付门禁在最终报告中仍为失败；
- 未关闭的 `critical` 或 `major`。

机器不得根据创造性、洞察、应用价值、表达质量、视觉美感或竞争力分数直接决定 `READY/BLOCKED`。

### 3.2 Reviewer 判断事项

以下由独立 Reviewer 基于论文和证据判断，不包装成 Python 事实：

- 模型是否具有针对性、创造性与洞察；
- 论证是否清楚、完整、有说服力；
- 图表是否达到高质量视觉沟通；
- 方案是否具有应用价值；
- 获奖竞争力分数、等级和改进优先级。

Reviewer 仍可把明确影响正确性、理解或提交安全的缺陷记为 `critical` 或 `major`；单纯得分不高不能自动产生阻断项。

## 4. 保留的篇幅与图表数量门禁

图数与表数下限由 Core 固定为本节契约的 `body_figure_minimum` 和 `body_table_minimum`，对任何赛事与文字系统一律成立；字数下限、页数上下限及其统计口径由当前项目赛事 profile 的工作区设定段提供（`body_word_minimum`、`body_page_minimum`、`body_page_maximum`，缺省或 `0` 表示该方向不限）。本节只固定这些门禁的存在与执行方式：

1. 叙述性正文必须通过 `PW-LEN-001` 的字数下限；
2. 被统计区段内的编号图不少于 `body_figure_minimum`、编号表不少于 `body_table_minimum`；
3. 页数服从 profile 声明的上下限。**统计区段由该 profile 定义**——不同赛事计的是不同区段（例如只计正文段与计整份提交 PDF 是两套口径），换赛事时必须连口径一起换，不得只改数字；
4. 统计区段由论文源中两组标签定界，位置由该 profile 的口径段决定：`page:counted-first`／`page:counted-last` 定页数与编号图表区段，`text:counted-first`／`text:counted-last` 定字数区段（仅当声明 `body_word_minimum` 时需要，两者口径可以不同）。审计脚本从 `06-paper/main.aux` 读 `page:*` 页号得出起止页与页数，并以拟交付 PDF 总页数核对；编号图表在 `page:*` 区段内计数，字数在 `text:*` 区段内按 `PW-LEN-001` 计数法统计（剥去注释、公式与浮动体）。缺标签、缺 `main.aux` 或无法定界一律 MAJOR，不得人自报；最终审校因此必须排在编译之后、清理之前；
5. 不得用无关文字、重复或装饰图表、拆分图号、缩小字号、压缩行距或缩窄页边距凑门禁；只有承担 `PW-FIG-001` 论证职责的编号图和编号表才计入。

任一项失败至少记为 `major` 并阻断发布。

## 5. 一次性最终 PDF 与图片检查

Final Audit 只做一次拟交付 PDF 的逐页渲染，并在同一遍中执行 `PW-FMT-001`、`PW-FIG-001`、论文写作规范的匿名性要求和 `WG-RELEASE-001` 的交付路由。图片尺寸、字号与拥挤程度须在该 PDF 的实际显示比例（100%）下判定，不得只按源图或缩放视图判断。各控制项的具体检查内容只在对应权威文件定义；质量评分、图片过程记录和发布报告不得再维护平行逐图清单。

## 6. 获奖竞争力评分（非阻断）

各赛事公开的评阅导向普遍强调假设合理性、建模创造性、结果正确性和表达清晰程度，但没有一套公开固定、可保证获奖的百分制。本表仅用于内部严格预审：

| 维度 | 分值 | 核心问题 |
|---|---:|---|
| 问题理解与假设合理性 | 15 | 是否抓住题意、约束和现实机制，假设是否必要并得到回扣 |
| 建模创造性与方法适配 | 25 | 是否有实质洞察，复杂度是否必要，各问是否形成递进体系 |
| 结果正确性与证据强度 | 25 | 结果是否可追溯、可复算，并经过适用验证 |
| 表达清晰度与视觉沟通 | 15 | 摘要、论证、公式和图表是否清楚且服务论点 |
| 求解、验证与可复现性 | 10 | 算法与参数是否足以复核，是否满足 `PW-VAL-001` |
| 完成度、应用价值与推广 | 10 | 是否逐问作答，方案是否可执行，局限与推广是否具体 |
| **合计** | **100** | |

每个维度给出得分、扣分理由、精确论文位置、证据和下一步改进。不得因排版精美给正确性加分，也不得因算法名称新颖给创造性加分。

| 总分 | 内部等级 | 参考判断 |
|---:|---|---|
| 92—100 | A+ | 具有较强的当届最高奖竞争力 |
| 85—91 | A | 达到内部获奖竞争力参考线 |
| 75—84 | B | 尚未达到参考线 |
| 60—74 | C | 存在明显短板 |
| <60 | D | 建议系统性重构 |

总分 85、“建模创造性与方法适配”20/25、“结果正确性与证据强度”21/25、“表达清晰度与视觉沟通”12/15 继续作为诊断参考线，同时还应查看逐问回答、`PW-VAL-001` 和实质亮点。无论是否达到这些参考线，都不得由 Python 据此阻断发布，也不得把内部评分写成官方获奖保证。

## 7. 发现项分级

- `critical`：伪造或不可追溯的核心结果/引用；关键程序无法复现或与论文冲突；泄露身份；违反官方硬规则；遗漏题目核心输出。
- `major`：核心证据、验证、交付、篇幅图表门禁或关键模型条件失败，足以影响正确性、可理解性、复现或提交安全。
- `minor`：不改变结论的局部格式、措辞或轻微视觉问题；是否必须在提交前关闭由其实际影响决定。
- `note`：竞争力提升建议或可选改进，不影响发布。

竞争力维度得分低原则上形成 `note` 或改进建议；只有同时存在可定位的硬错误时才升级为 `major`。

## 8. 最终报告（`PQA-REPORT-001`）

`07-review/final-audit.md` 以 `## 机器可读摘要` 起头，每行一个 `- <字段>: <值>`，字段名与顺序即本文件契约的 `final_audit_fields`。取值制度：`audit_date` 为 `YYYY-MM-DD`，`audit_phase` 为 `RELEASE_CANDIDATE` 或 `FINAL`，`review_scope` 为 `FULL` 或 `IMPACTED`，`release_decision` 为 `READY` 或 `BLOCKED`；四个 gate 字段取 `PASS` 或 `BLOCKED`，`clean_reproduction_gate` 另可取 `REUSED_UNCHANGED`；`open_critical` 与 `open_major` 为整数；`final_pdf` 指向 `08-delivery/` 的拟交付 PDF，`final_pdf_sha256` 为其 64 位十六进制哈希。篇幅与图表数量不进入报告字段——起止页、页数、字数、图号和表号由审计脚本按第 4 节从论文源、`main.aux` 与拟交付 PDF 导出，人不得自报。

摘要内同一字段只允许出现一次，重复即 MAJOR，后写取值不得覆盖前写。`open_critical` 与 `open_major` 必须等于 `07-review/review-log.md` 中状态属于契约 `review_open_statuses` 的对应严重级行数。

正文继续记录：规则核对日期与来源、clean reproduction 命令和证据、关键结果比对、PDF/图片检查范围、发现项、修改影响分析、竞争力评分和免责声明。机器不解析竞争力评分或主观视觉维度。

Final 阶段使用 `IMPACTED` 时，报告必须指向上一轮完整 RC 审查，列明变更文件、受影响页面/图表、关键文件存在状态、阶段完成状态、未受影响计算的理由，以及本次实际复查内容；不得要求中间文件哈希作为复用依据。

## 9. 发布门禁（`PQA-RELEASE-001`）

只有以下条件全部满足才可发布：

- 当届官方规则、匿名性和交付完整性通过；
- 核心结果正确，证据真实存在且论文与机器结果一致；
- clean reproduction 已成功，或 Final 阶段有充分证据复用未变化的 RC 结果；
- `PW-LEN-001`、正文页数、图数和表数门禁通过；
- `docs/standards/modeling-execution.md` 的 `PW-VAL-001` 与 `PW-FIG-001` 的实质检查通过；
- 最终 PDF 哈希对应实际审查对象；
- 无未关闭的 `critical` 或 `major`。

获奖竞争力总分、等级和维度参考线不属于本发布门禁。未达到参考线时应明确报告短板和建议，但只要上述硬条件通过，`release_decision` 可以为 `READY`。
