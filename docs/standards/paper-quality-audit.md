# 数学建模论文质量审查标准

> 适用范围：项目 `07-review/` 中的论文质量审查、国奖竞争力评估和发布门禁。
>
> 核心原则：**合规通过不等于具有国奖竞争力；国奖竞争力判断也不能替代竞赛硬性合规检查。**

---

## 1. 权威边界

论文质量审查必须同时依据：

1. `docs/standards/cumcm-current-rules.md` 中已重新核验的当届全国组委会规则及赛题要求；
2. `docs/standards/paper-writing.md`；
3. `docs/standards/paper-figures.md`；
4. 项目题面、数据、代码、结果和证据索引；
5. 本标准的国奖竞争力评分口径。

全国组委会现行章程将**假设的合理性、建模的创造性、结果的正确性和文字表述的清晰程度**列为主要评奖标准。全国奖项评阅的具体细则由评阅组结合当年赛题讨论确定，并不存在一套公开、固定且可保证获奖的百分制。因此，本文件给出的分数和等级是工作区内部的严格预审门槛，只表示“是否具备国奖竞争力”，不得写成“保证获得国奖”。

竞争力评分核对来源（2026-08-18）：

- [全国大学生数学建模竞赛章程](https://www.mcm.edu.cn/upload_cn/node/602/61izwQgK14526f4445eb73286aaa94a185f77b4b.pdf)；
- [全国大学生数学建模竞赛全国奖项评阅工作规范（2023 年修订稿）](https://www.mcm.edu.cn/html_cn/node/b1f48689659f0660e80a2d6279d7b37d.html)。

格式与提交来源统一见 `OFFICIAL-CUMCM-001`。正式提交前必须重新核对官网；当届新规高于本标准。

---

## 2. 审查独立性与输出

1. 质量审查由独立于当前写作过程的审查步骤执行，不接受作者自述作为通过证据。
2. 审查对象必须是拟交付的最终 PDF，同时核对权威论文源、题面、证据索引、代码和机器结果。
3. 每个项目必须在 `07-review/paper-quality-audit.md` 保存质量审查报告；发现项同步登记到 `07-review/review-log.md`。
4. 每次论文、图表或关键结果发生实质修改后，旧结论自动失效，必须更新 PDF 哈希、复查受影响页面并重新给出结论。
5. 报告必须分别给出“`paper-writing.md` 合规结论”“`paper-figures.md` 合规结论”和“国奖竞争力结论”，不得只给总分。

---

## 3. 第一门：论文与图片规范合规审查

逐条核对 `paper-writing.md` 与 `paper-figures.md` 的全部“必须 / 不得”和最终交付检查表，至少覆盖：

- `WG-MODEL-001` 与 `PWL-GATE-001` 已通过；
- 题目完成度、章节结构、摘要专页、正文与附录分页；
- 每问的问题转化、变量指标、局部推导、完整模型汇总、求解和直接答案；
- `WG-EVID-001` 与 `PW-VAL-001` 已通过；
- 表格要求与 `PW-FIG-001` 均已通过；
- 公式、符号、单位、有效数字、字体和全文一致性；
- 文献真实性、正文实际引用、指定教材、AI 披露和匿名性；
- 最终 PDF 的逐页渲染、字体属性、页边距、溢出、重叠和交付完整性。

### 3.1 正文篇幅与图表数量硬性门禁

以下要求是本工作区新增的论文质量门禁，不冒充全国组委会统一规定；当届官方或赛区要求更严格时，从其规定：

1. 正文叙述性内容必须通过 `docs/standards/paper-writing.md` 的 `PW-LEN-001`；审查报告必须记录统计工具、统计范围和统计结果。
2. 正文必须至少包含 **5 个图**和 **3 个表**。只统计正文中已编号、被正文实际引用并承担分析、建模、求解、结果或验证功能的图表；附录图表不计。一个多子图组合按一个图号计，跨页延续的同一张表按一个表号计。重复、拆分或装饰性图表不得用于凑数。
3. 正文必须为 **20—30 页**，上下限均包含。页数从摘要专用页后的“问题重述”首页起，计算至“参考文献”末页止；摘要专用页和全部附录不计入正文页数。
4. 审查必须以拟交付最终 PDF 为准，记录正文起止页、正文页数、正文统计字数、图号清单和表号清单。仅依据源文件估算不得判定通过。
5. 任一项不满足，至少记为 `major`，`paper_writing_compliance` 必须判为 `BLOCKED`，并阻断发布。不得通过缩小字号、压缩行距、缩窄页边距、重复图表、拆分图号或填充无关文字满足数量要求。

`paper_writing_compliance` 与 `paper_figure_compliance` 的结论均只能为：

- `PASS`：所有硬性项通过，且不存在未关闭的 `critical` 或 `major`；
- `BLOCKED`：任一硬性项失败，或存在未关闭的 `critical` / `major`。

任一合规结论为 `BLOCKED` 时，不得判为达到国奖竞争力门槛，无论总分多高。

---

## 4. 第二门：国奖竞争力评分

### 4.1 百分制维度

| 维度 | 分值 | 核心问题 |
|---|---:|---|
| 问题理解与假设合理性 | 15 | 是否准确抓住题意、约束和现实机制；假设是否必要、可解释并在评价中回扣 |
| 建模创造性与方法适配 | 25 | 是否有实质建模洞察；模型是否针对题目而非堆砌算法；复杂度是否必要；各问是否形成递进体系 |
| 结果正确性与证据强度 | 25 | 数值和结论是否可追溯、可复算；约束、量纲、边界、基准、误差和稳健性是否充分支撑结论 |
| 表达清晰度与视觉沟通 | 15 | 摘要是否高信息密度；论证是否顺畅；公式和图表是否清晰、直观、无歧义且服务论点 |
| 求解、验证与可复现性 | 10 | 算法细节是否足以复核；代码、参数、日志和产物是否一致；是否满足 `PW-VAL-001` |
| 完成度、应用价值与推广 | 10 | 是否逐问直接作答；方案是否可执行；局限、改进和推广是否具体而克制 |
| **合计** | **100** | |

### 4.2 评分证据

每个维度必须写出：

- 得分与扣分理由；
- 至少一个精确论文位置；
- 对应数据、代码、图表、日志或文献证据；
- 若未满分，达到下一等级所需的具体改进。

不得因排版精美给模型正确性加分，也不得因算法名称新颖给创造性加分。创新必须落实为新的问题转化、结构设计、约束处理、验证方法或有证据的性能增益。

### 4.3 等级与判定

| 总分 | 内部等级 | 国奖竞争力结论 |
|---:|---|---|
| 92--100 | A+ | 具有较强的全国一等奖竞争力 |
| 85--91 | A | 达到国奖竞争力门槛 |
| 75--84 | B | 尚未达到国奖竞争力门槛 |
| 60--74 | C | 论文质量存在明显短板 |
| <60 | D | 需要系统性重构 |

判为 `MEETS_NATIONAL_AWARD_COMPETITIVE_STANDARD` 必须同时满足：

1. `paper-writing.md` 与 `paper-figures.md` 合规结论均为 `PASS`；
2. 无未关闭的 `critical` 或 `major`；
3. 总分不低于 85；
4. “建模创造性与方法适配”不低于 20/25，“结果正确性与证据强度”不低于 21/25，“表达清晰度与视觉沟通”不低于 12/15；
5. 每问均被直接回答，并通过 `PW-VAL-001`；
6. 至少有一项可定位、非装饰性的实质亮点，且其作用有结果或推导支撑。

缺一项即结论为 `DOES_NOT_MEET_NATIONAL_AWARD_COMPETITIVE_STANDARD`。A+ 仅表示更强内部预审结果，仍不构成获奖承诺。

---

## 5. 图片专项审查

### 5.1 检查方法

图片的图型、比例、字号、格式、颜色、内容和三层视觉自检只以 `PW-FIG-001` 为准。本审查步骤不重复这些参数，只负责独立执行：

1. 从拟交付 PDF 建立图片清单并逐项执行 `PW-FIG-001`；
2. 在报告中记录页码、图号、用途、语义合规、形式合规、视觉合规、与正文一致性和结论；
3. 修复后按 `PW-FIG-001` 的失效规则重新渲染并复查。

### 5.2 硬性通过条件

只有全部适用图片通过 `PW-FIG-001`，`paper_figure_compliance` 才能为 `PASS`。任何 `PW-FIG-001` 阻断情形至少记为 `major` 并阻断发布；不影响理解的轻微装饰性偏差可记为 `minor`，但正式交付前仍应关闭。

---

## 6. 发现项与报告格式（`PQA-REPORT-001`）

每项发现必须包含：

`id`、`severity`、`location`、`criterion`、`finding`、`evidence`、`required_fix`、`verification`、`status`。

`07-review/paper-quality-audit.md` 至少采用以下结构：

```markdown
# 论文质量审查报告

## 机器可读门禁

- audit_date: `YYYY-MM-DD`
- final_pdf: `08-delivery/paper.pdf`
- final_pdf_sha256: `<64 位 SHA-256>`
- body_word_count: `<整数，必须满足 PW-LEN-001>`
- body_page_range: `<起始页-结束页>`
- body_page_count: `<整数，执行本标准第 3.1 节>`
- body_figure_count: `<整数，执行本标准第 3.1 节>`
- body_table_count: `<整数，执行本标准第 3.1 节>`
- body_length_and_visual_count_gate: `PASS` 或 `BLOCKED`
- paper_writing_compliance: `PASS` 或 `BLOCKED`
- paper_figure_compliance: `PASS` 或 `BLOCKED`
- national_award_competitiveness: `MEETS_NATIONAL_AWARD_COMPETITIVE_STANDARD` 或 `DOES_NOT_MEET_NATIONAL_AWARD_COMPETITIVE_STANDARD`
- full_pdf_render_review: `PASS`
- figure_clarity_and_intuitiveness: `PASS`
- overlap_and_clipping: `PASS`
- flowchart_logic: `PASS` 或 `NOT_APPLICABLE`
- open_critical: `0`
- open_major: `0`
- open_presentation_minor: `0`
- release_decision: `READY` 或 `BLOCKED`

对照版本：paper-writing.md / paper-figures.md / paper-quality-audit.md / 当届官方规则

## 一、结论
- paper-writing.md 合规：PASS / BLOCKED
- paper-figures.md 合规：PASS / BLOCKED
- 国奖竞争力：MEETS... / DOES_NOT_MEET...
- 总分与等级：
- 发布决定：READY / BLOCKED

## 二、硬性合规矩阵
| 类别 | 结论 | 证据 | 未关闭问题 |

## 三、国奖竞争力评分
| 维度 | 得分 | 证据 | 扣分与提升要求 |

## 四、图片逐项审查
| 页码/编号 | 用途 | 清晰 | 直观 | 无重叠 | 与正文一致 | 结论 |

## 五、发现项
按 critical、major、minor、note 排列。

## 六、最终判定依据与免责声明
说明本结论是内部竞争力预审，不构成官方获奖保证。
```

机器可读门禁字段必须逐项保留、使用反引号包裹值，且与正文结论一致。自动脚本只验证报告存在、字段完整、PDF 哈希一致和阻断项计数；“清晰、直观、无重叠”等结论仍必须来自真实逐页渲染和人工视觉检查，不得用脚本通过替代目视审查。

---

## 7. 发布门禁（`PQA-RELEASE-001`）

满足以下全部条件才可发布：

- `paper-writing.md` 合规为 `PASS`；
- `paper-figures.md` 合规为 `PASS`，即 `paper_figure_compliance` 为 `PASS`；
- `PW-LEN-001` 与本标准第 3.1 节均通过，且 `body_length_and_visual_count_gate` 为 `PASS`；
- 质量审查报告存在，且 PDF 哈希与拟交付文件一致；
- 机器可读门禁中的逐页渲染、图形清晰直观、重叠裁切和流程逻辑检查均为 `PASS` 或适用时为 `NOT_APPLICABLE`；
- 所有 `critical`、`major` 和影响正式呈现的 `minor` 已关闭；
- 最终 PDF 已逐页复查，所有图表清晰、直观、无重叠；
- 若项目目标明确为国奖竞争力，结论必须为 `MEETS_NATIONAL_AWARD_COMPETITIVE_STANDARD`，否则继续改进或由用户明确接受降级交付。
