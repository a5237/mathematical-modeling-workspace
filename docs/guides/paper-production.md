# 数学建模论文生产系统

本系统把赛题处理拆成“题目—模型—代码—结果—证据—论文—审校—交付”八层，核心目标是让每个数字、图表、结论和引用都可追溯、可复现、可审计。

## 快速使用

创建新项目：

```powershell
.\.venv-modeling\Scripts\python.exe .\.codex\skills\cumcm-paper-production\scripts\init_cumcm_project.py --root workspace\projects --contest cumcm --year 2026 --problem a
```

初始化脚本会将 `resources/templates/cumcm-paper-framework.tex` 复制为项目 `06-paper/main.tex`，并将 `resources/templates/figure-selection-record.md` 复制为 `00-admin/figure-selection-record.md`。完成写作门禁后直接在论文副本上持续写作和修订；普通图片只在轻量 registry 登记一行，潜在误导性视觉处理才展开说明。

完成计算后，把论文中的关键主张登记到 `05-evidence/evidence-index.csv`，把文献登记到 `05-evidence/literature-ledger.csv`。Draft 阶段可运行静态提示：

```powershell
.\.venv-modeling\Scripts\python.exe .\.codex\skills\cumcm-paper-audit\scripts\audit_cumcm_project.py workspace\projects\cumcm-2026-a --phase draft
```

内容冻结为 Release Candidate 后，由 Final Audit 完成唯一一次 clean reproduction、最终 PDF 逐页/逐图检查并写入 `07-review/final-audit.md`，随后运行客观 preflight：

```powershell
.\.venv-modeling\Scripts\python.exe .\.codex\skills\cumcm-paper-audit\scripts\audit_cumcm_project.py workspace\projects\cumcm-2026-a --phase release-candidate
```

Final 阶段发生修改时按影响范围复查，再用 `--phase final` 核对报告与交付物。退出码为 0 只表示客观静态门禁通过；不能替代 clean reproduction、最终 PDF 读图和独立 Reviewer 判断。

Agent 阶段顺序与停止条件只以 `.codex/skills/cumcm-paper-production/SKILL.md` 为准；本指南只保留用户命令。各门禁及权威分工见 `docs/README.md`。
