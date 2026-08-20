# 审校分级

- `critical`：伪造或不可追溯结果/引用；程序无法运行或与论文不符；泄露身份；违反竞赛硬性规则；遗漏题目要求的核心输出。
- `major`：不满足 `WG-MODEL-001`、`PWL-GATE-001`、`WG-EVID-001`、`PW-VAL-001` 或论文硬性要求；摘要与正文数值冲突；关键约束、单位、参数或交付材料缺失；最终 PDF 中存在影响文字识别、连接关系或判断逻辑的图文重叠、裁切、模糊或流程歧义。
- `minor`：不改变结论的编号、措辞或局部格式问题；不影响理解的轻微视觉偏差。正式交付前仍应关闭所有影响呈现质量的 `minor`。
- `note`：可选改进，不影响提交。

报告每项包含：`id`、`severity`、`location`、`finding`、`evidence`、`required_fix`、`verification`。先列阻断项，再给总分。存在 `critical` 或 `major` 时，结论只能是 `BLOCKED`。

发布分级使用本文件；论文质量与国奖竞争力评分统一使用 `docs/standards/paper-quality-audit.md`，不得维护第二套冲突权重。硬性违规优先于分数。
