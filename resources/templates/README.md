# 通用模板

保存未填写的论文、报告、清单和表格模板。

- `contests/<profile>/paper-framework.tex`：`docs/standards/paper-writing.md` 与 `docs/standards/paper-formatting.md` 在对应赛事下的 LaTeX 实现；初始化时复制为项目 `06-paper/main.tex`。
- `figure-selection-record.md`：`PW-FIG-001` 的轻量记录实现。
- `final-audit-record.md`：`PQA-REPORT-001` 的最终报告实现；机器可读摘要的字段行由初始化器按契约 `final_audit_fields` 顺序生成，不在模板里手写清单。
- `artifact-map.yaml`：`WG-ROUTE-001` 的项目导航实现；通用影响关系从权威 machine contract 读取，不在模板复制。

使用与更新边界分别执行 `WG-ROUTE-001`、`PW-FIG-001`、`PQA-REPORT-001` 及论文写作规范；本入口不重复模板覆盖、审查生命周期或报告规则。
