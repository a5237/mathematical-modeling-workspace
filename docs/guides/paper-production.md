# 论文生产系统

本系统把赛题处理拆成“题目—模型—代码—结果—证据—论文—审校—交付”八层，核心目标是让每个数字、图表、结论和引用都可追溯、可复现、可审计。

## 快速使用

创建新项目（`--contest` 取值只认 `config/contests/<profile>/profile.yaml` 中 `contests` 列表声明的赛事标识，当前为 `cumcm`、`mcm`、`icm`；profile 目录名如 `mcm-icm` 不是赛事标识）：

```powershell
.\.venv-modeling\Scripts\python.exe .\.codex\skills\modeling-paper-production\scripts\init_modeling_project.py --root workspace\projects --contest cumcm --year 2026 --problem a
.\.venv-modeling\Scripts\python.exe .\.codex\skills\modeling-paper-production\scripts\init_modeling_project.py --root workspace\projects --contest mcm --year 2027 --problem c
```

初始化器的目录、模板和记录行为分别执行 `LAYOUT-001`、`WG-ROUTE-001`、`PWL-GATE-001` 与 `PW-FIG-001`；本指南只提供命令入口。

客观静态检查与 preflight 命令同一条，`--phase` 取 `draft`、`release-candidate` 或 `final`：

```powershell
.\.venv-modeling\Scripts\python.exe .\.codex\skills\modeling-paper-audit\scripts\audit_modeling_project.py workspace\projects\cumcm-2026-a --phase release-candidate
```

阶段含义与复查范围只以 `PQA-REPORT-001` 与 `PQA-RELEASE-001` 为准。审校脚本的退出码：`0` 为静态 preflight 通过，`1` 为存在阻断项，`2` 为权威契约错误（契约错误不产 finding，须先修权威文件）。`--root` 给出相对路径时按工作区根目录解析，与当前所在目录无关。

Agent 阶段顺序与停止条件只以 `.codex/skills/modeling-paper-production/SKILL.md` 为准；本指南只保留用户命令。各门禁及权威分工见 `docs/README.md`。
