# 命名与文件格式规范

本文是 Agent 的唯一普通命名权威。项目名、inbox 名、`q01`、图表标签等低风险命名不设置独立 Python hard gate；只有名称会导致路径无法解析、程序不能运行、文件冲突、证据不可追溯或正式提交违规时才由机器阻断。

## 项目标识

- 项目目录：`<contest>-<year>-<problem>`，全部小写，例如 `cumcm-2026-a`。
- 子问题编号：`q01`、`q02`，不要使用“问题1”“第一问”等不稳定路径名。
- 文件名仅使用小写 ASCII 字母、数字和连字符；扩展名保持小写。
- 文中中文标题不受此限制；提交文件名另以当年官方要求为准。

## 推荐目录名

初始化器默认创建 `00-admin` 至 `08-delivery`；完整推荐树、扩展方式和职责只以 `docs/architecture/workspace-layout.md` 为准。项目可按题目增加或拆分内部目录，审计不把该骨架当作完整 schema。

## 产物命名

- 程序：`q01-<purpose>.py`，入口优先为 `run-all.py`。
- 模型与算法选择记录：`03-models/model-selection.md`。
- 写作前学习记录：`00-admin/pre-writing-learning.md`。
- 图片 registry 与高风险视觉说明：`00-admin/figure-selection-record.md`。
- 参数：`q01-parameters.yaml`；随机种子必须显式记录。
- 表格：`q01-table-001-<topic>.csv`。
- 图片文件名主干：`q01-figure-001-<topic>`；扩展名与正式导出组合执行 `docs/standards/paper-figures.md` 的 `PW-FIG-001`。
- 指标：`q01-metrics.json`。
- 日志：`q01-run-<yyyymmddThhmmss>.log`。
- 通用论文框架：`resources/templates/cumcm-paper-framework.tex`；复制到正式项目后固定命名为 `06-paper/main.tex`。
- 论文源文件：`main.tex`；文献库：`references.bib`。
- 审稿台账：`review-log.md`；RC 与 Final 的唯一最终审查报告：`final-audit.md`。旧项目的 `release-audit.md`、`paper-quality-audit.md` 只作历史记录，不再产生新的平行结论。

## 稳定标识

- 主张：`C-Q01-001`。
- 证据：`E-Q01-001`。
- 文献：BibTeX key 使用 `author-year-keyword`。
- 图、表、公式标签：`fig:q01-*`、`tab:q01-*`、`eq:q01-*`。

不得把“final”“最终版”“最新版”用作版本号。版本由 Git 提交记录管理；发布副本使用明确日期或竞赛要求的命名。
