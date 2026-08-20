# 数学建模论文生产系统

本系统把赛题处理拆成“题目—模型—代码—结果—证据—论文—审校—交付”八层，核心目标是让每个数字、图表、结论和引用都可追溯、可复现、可审计。

## 快速使用

创建新项目：

```powershell
.\.venv-modeling\Scripts\python.exe .\.codex\skills\cumcm-paper-production\scripts\init_cumcm_project.py --root workspace\projects --contest cumcm --year 2026 --problem a
```

完成计算后，把论文中的关键主张登记到 `05-evidence/evidence-index.csv`，把文献登记到 `05-evidence/literature-ledger.csv`。发布前运行：

```powershell
.\.venv-modeling\Scripts\python.exe .\.codex\skills\cumcm-paper-audit\scripts\audit_cumcm_project.py workspace\projects\cumcm-2026-a --phase release
```

退出码为 0 才表示通过自动门禁；自动检查不能替代人工阅读和重新运行模型。

建模、写作和发布的启动条件分别执行 `WG-MODEL-001`、`PWL-GATE-001` 和 `PQA-RELEASE-001`。本指南只说明用户操作顺序，不重新定义模型数量、学习数量、论文格式或审校阈值。

## 阶段门禁

1. `intake`：题目、附件、问题清单齐全。
2. `design`：问题设计完成并通过 `WG-MODEL-001`。
3. `compute`：代码可运行，随机种子、参数、环境和日志已保存。
4. `validate`：结果与证据通过 `WG-EVID-001` 和 `PW-VAL-001`。
5. `write`：`PWL-GATE-001` 已通过，按 `docs/standards/paper-writing.md` 从核验证据写作。
6. `audit`：由独立审校流程检查一致性、引用、匿名性和格式。
7. `release`：`OFFICIAL-CUMCM-001` 与 `PQA-RELEASE-001` 均已通过。

完整权威分工见 `docs/README.md`：命名、工程与复现、证据、论文内容与排版、官方规则、学习流程和质量审查分别以矩阵指定文件为准。
