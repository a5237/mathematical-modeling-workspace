# 命名与文件格式规范

## 项目标识

- 项目目录：`<contest>-<year>-<problem>`，全部小写，例如 `cumcm-2026-a`。
- 子问题编号：`q01`、`q02`，不要使用“问题1”“第一问”等不稳定路径名。
- 文件名仅使用小写 ASCII 字母、数字和连字符；扩展名保持小写。
- 文中中文标题不受此限制；提交文件名另以当年官方要求为准。

## 标准目录

```text
cumcm-2026-a/
├── 00-admin/       # 项目清单、环境、运行记录、写作前学习记录
├── 01-problem/     # 原题副本、附件清单、问题清单
├── 02-data/        # raw 只读；processed 可再生
├── 03-models/      # 模型选择记录、q01、q02…模型代码与参数
├── 04-results/     # tables、figures、metrics、logs
├── 05-evidence/    # 主张证据、文献、AI 使用台账
├── 06-paper/       # tex、bib、图片引用与编译产物
├── 07-review/      # 自动审计、发布审校与论文质量审查记录
└── 08-delivery/    # 最终论文与支撑材料副本
```

## 产物命名

- 程序：`q01-<purpose>.py`，入口优先为 `run-all.py`。
- 模型与算法选择记录：`03-models/model-selection.md`。
- 写作前学习记录：`00-admin/pre-writing-learning.md`。
- 参数：`q01-parameters.yaml`；随机种子必须显式记录。
- 表格：`q01-table-001-<topic>.csv`。
- 图片：`q01-figure-001-<topic>.png`，建议同时保留 PDF/SVG 矢量版。
- 指标：`q01-metrics.json`。
- 日志：`q01-run-<yyyymmddThhmmss>.log`。
- 论文源文件：`main.tex`；文献库：`references.bib`。
- 审稿台账：`review-log.md`；发布审校：`release-audit.md`；论文质量与国奖竞争力审查：`paper-quality-audit.md`。

## 稳定标识

- 主张：`C-Q01-001`。
- 证据：`E-Q01-001`。
- 文献：BibTeX key 使用 `author-year-keyword`。
- 图、表、公式标签：`fig:q01-*`、`tab:q01-*`、`eq:q01-*`。

不得把“final”“最终版”“最新版”用作版本号。版本由 Git 提交记录管理；发布副本使用明确日期或竞赛要求的命名。
