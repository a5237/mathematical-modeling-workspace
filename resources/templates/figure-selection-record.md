# 图片注册表与高风险视觉处理说明

> 本表只用于追踪正式论文图片，不是候选图审批单。普通图片登记一行即可；图型选择、科学正确性和最终 PDF 审查执行 `PW-FIG-001`。

- project_id: `待填写`
- record_updated_at: `YYYY-MM-DD`

## 一、正式图片 registry

| figure_label | question_or_purpose | authoritative_source | generator | selected_structure_or_chart | result_artifact | paper_copy | final_pdf_page | final_pdf_check |
|---|---|---|---|---|---|---|---|---|
| `fig:q01-*` | 待填写 | 项目相对路径或模型定义 | 项目相对路径或推导说明 | 待填写 | `04-results/figures/...` | `06-paper/figures/...` | 待定 | `PENDING` |

填写原则：

- 图型首先服从数据结构、模型原生结构、科学含义、论文论证和信息表达效率；
- 不得因为容易生成、记录较少或审查简单而把适合响应面、等高线、空间场、流线、相图、Pareto 前沿、网络、Sankey、科学三维、多面板或轨迹的结果降级成简单图；
- 复杂本身不是风险，上述图型与普通折线图使用同一行登记；
- 程序生成的正式图片在 `result_artifact` 中登记同内容的 PNG 与 SVG 文件；真实栅格图不做无意义矢量化时按 `PW-FIG-001` 记录实际 PNG 文件；
- `final_pdf_check` 只记录最终 PDF 中的 `PASS` 或 `BLOCKED`，生产过程预览无需维护额外 verdict。

## 二、高风险视觉处理说明

只有使用下列处理时才填写本节：双 Y 轴、断轴或明显截断坐标、强平滑、大规模抽样或删点、特殊聚合、非标准归一化、可能改变判断的视觉变换，或存在明显解释歧义的复合编码。

| figure_label | risk_trigger | scientific_necessity | alternatives_considered | parameters_and_scope | disclosure_location | validation | decision |
|---|---|---|---|---|---|---|---|

若没有上述处理，删除本节。

## 三、整组视觉语言（按需）

- style_reference_ids：按整组图片登记实际使用的参考项；未使用参考图时删除本节。
- adopted_style_attributes：只记录实际借鉴的字体层级、轴线、配色、线点尺度、留白、图例或多面板属性。
- explicitly_not_copied：确认未复制参考图的数据、模型、结构、结论和注释。

## 四、交接检查

- [ ] 每张实际入文图片均能追溯到权威数据、程序或模型定义。
- [ ] 图片、正文、公式、表格、附录与机器结果口径一致。
- [ ] 涉及潜在误导的视觉处理已有必要说明。
- [ ] 最终 PDF 中全部图片已按 `PW-FIG-001` 检查，失败项已回到生成源修复。
