# 论文生产系统

本系统把赛题处理拆成“题目—模型—代码—结果—证据—论文—审校—交付”八层，核心目标是让每个数字、图表、结论和引用都可追溯、可复现、可审计。

## 快速使用

创建新项目：

```powershell
.\.venv-modeling\Scripts\python.exe .\.codex\skills\cumcm-paper-production\scripts\init_cumcm_project.py --root workspace\projects --contest cumcm --year 2026 --problem a
```

初始化器的目录、模板和记录行为分别执行 `LAYOUT-001`、`WG-ROUTE-001`、`PWL-GATE-001` 与 `PW-FIG-001`；本指南只提供命令入口。

Draft 阶段的客观静态检查命令：

```powershell
.\.venv-modeling\Scripts\python.exe .\.codex\skills\cumcm-paper-audit\scripts\audit_cumcm_project.py workspace\projects\cumcm-2026-a --phase draft
```

Release Candidate 阶段的客观 preflight 命令：

```powershell
.\.venv-modeling\Scripts\python.exe .\.codex\skills\cumcm-paper-audit\scripts\audit_cumcm_project.py workspace\projects\cumcm-2026-a --phase release-candidate
```

Final 阶段使用同一命令的 `--phase final`；阶段含义、复查范围和退出码边界只以 `PQA-REPORT-001` 与 `PQA-RELEASE-001` 为准。

Agent 阶段顺序与停止条件只以 `.codex/skills/cumcm-paper-production/SKILL.md` 为准；本指南只保留用户命令。各门禁及权威分工见 `docs/README.md`。
