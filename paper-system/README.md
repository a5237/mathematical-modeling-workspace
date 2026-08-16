# 数学建模论文生产系统

本系统把赛题处理拆成“题目—模型—代码—结果—证据—论文—审校—交付”八层，核心目标是让每个数字、图表、结论和引用都可追溯、可复现、可审计。

## 快速使用

创建新项目：

```powershell
.\.venv-modeling\Scripts\python.exe .\.codex\skills\cumcm-paper-production\scripts\init_cumcm_project.py --root projects --contest cumcm --year 2026 --problem a
```

完成计算后，把论文中的关键主张登记到 `05-evidence/evidence-index.csv`，把文献登记到 `05-evidence/literature-ledger.csv`。发布前运行：

```powershell
.\.venv-modeling\Scripts\python.exe .\.codex\skills\cumcm-paper-audit\scripts\audit_cumcm_project.py projects\cumcm-2026-a --phase release
```

退出码为 0 才表示通过自动门禁；自动检查不能替代人工阅读和重新运行模型。

## 阶段门禁

1. `intake`：题目、附件、问题清单齐全。
2. `design`：每问输入、输出、指标、候选模型和选择理由齐全。
3. `compute`：代码可运行，随机种子、参数、环境和日志已保存。
4. `validate`：每问至少完成两项适用的结果分析、误差分析、模型检验、灵敏度/稳健性分析或等效验证，且均有运行产物或可核验推导支撑。
5. `write`：证据索引先于具体数值写作，图表均有解释。
6. `audit`：由独立审校流程检查一致性、引用、匿名性和格式。
7. `release`：论文、支撑材料、AI 使用详情和文件清单一致。

格式与写作门禁包括：摘要页独立、各附录分别新起一页、中文宋体、西文与数字 Times New Roman、摘要重点加粗、各子问题的模型汇总公式，以及不少于 6 篇参考文献；优化模型先列目标函数，下一行以 `s.t.` 集中列约束；《数学模型（第五版）》与《数学建模算法与应用》必须列入并在正文实际引用，其余至少 4 篇与题目直接相关。详细命名见 `NAMING.md`；工程与复现门禁以根目录 `数学建模工作区_Agent强制规范.md` 为准，论文内容与排版以 `数学建模论文写作_Agent强制规范.md` 为准。
