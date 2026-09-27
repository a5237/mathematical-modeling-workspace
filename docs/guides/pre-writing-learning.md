# 写作前强制学习流程

> control_id: `PWL-GATE-001`

```toml machine-contract
learning_complete_status = "COMPLETE"
learning_initial_status = "INCOMPLETE"
learning_sample_columns = ["item", "path_or_source", "problem_type", "structural_lessons", "prohibited_copying", "reviewed"]
learning_algorithm_columns = ["question_id", "resource_path", "definition_and_assumptions", "applicability", "code_review", "status"]
learning_paper_minimum = 2
```

上方字段只承载稳定、客观的机器参数；学习质量仍由 Agent 和最终审校依据正文判断。

本流程是正文写作启动门禁的唯一权威。每个正式项目必须先在 `00-admin/pre-writing-learning.md` 完成并标记学习记录，才可开始撰写正文或摘要；其它规范、Skill 和检查表只引用本控制编号，不重新定义阅读数量、状态或失效条件。

## 1. 确认学习范围

- 根据题目与各子问题的数学类型，确定需要学习的范文类别和算法类别。
- 核对 `03-models/model-selection.md` 已记录实际选用模型、算法资源路径、适用性检查和偏离理由；算法库检索、候选比较与库外偏离的判定执行 `docs/standards/modeling-execution.md` 的 `WG-MODEL-001`。

## 2. 学习同类优秀论文

1. 阅读数量下限由本文件契约的 `learning_paper_minimum` 固定，对所有赛事一致；赛事 profile 不声明该键，也不得覆盖它。
2. 结构、摘要组织与篇幅分配的学习只计**同赛事**样本；样本目录按当前 profile 解析（`resources/paper-library/00-format-layout/<profile>/`）。跨赛事样本只可用于数学方法与论证逻辑学习，不计入结构学习数量。
3. 在 `resources/paper-library/` 的方法类目中检索同题型的优秀论文并实际阅读，只提取摘要组织、问题数学化、模型建立、求解说明、结果分析、验证和图表叙事的逻辑。
4. 只学习结构、论证方式和表达策略，不复制原文、公式、数据、图表或结论。
5. 范文仅用于学习时记录在学习表；若要在正式论文中引用，仍须单独登记到 `05-evidence/literature-ledger.csv` 并核验其对具体主张的支持。

## 3. 复核算法知识

- 逐问在学习记录中登记所用算法的资源路径、定义与假设、适用性结论和代码复核状态，并确认其对应 `03-models/model-selection.md` 的选用结果。
- 算法本身的适用条件判断、库外补充和项目化改写要求执行 `docs/standards/modeling-execution.md`，本文件不重复定义。

## 4. 完成学习记录

在 `00-admin/pre-writing-learning.md` 至少记录：

- 赛题类型和每个子问题的写作重点；
- 已读同类优秀论文的路径或来源及所学结构；
- 已阅读的算法资源文件、适用性结论和代码复核情况；
- 可借鉴的论证与图表策略；
- 明确禁止复制的内容；
- 学习完成日期，并将 `learning_status` 更新为 `COMPLETE`。

若模型、主要算法或论文结构发生实质变化，可返回本阶段补充受影响的学习内容并重新确认完成状态；不绑定旧文件哈希，也不要求重做未受影响的学习记录。

## 5. 启动写作

仅在以下条件同时满足后开始正文写作：

- `WG-MODEL-001` 已达到建模执行规范定义的完成状态；
- `00-admin/pre-writing-learning.md` 的 `learning_status` 为 `COMPLETE`；
- 具体数值、图表和结论已有可核验产物并进入证据链；
- 写作遵循 `docs/standards/paper-writing.md`，图片遵循 `docs/standards/paper-figures.md`，不得把学习记录或工程路径原样写入正文。
