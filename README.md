# 全国大学生数学建模工作区

这是一个面向长期复用的数学建模工作区。仓库按“文档、配置、工具、资源、工作数据、运行时产物”分层，正式赛题仍在各自项目内使用 `00-admin` 至 `08-delivery` 的可复现生产结构。

## 仓库分层

```text
.
├── config/                 # 依赖锁定与工作区级配置
├── docs/                   # 架构、规范与操作指南
├── resources/              # 算法资料、模板和优秀论文参考库
├── tools/                  # 跨项目通用工具
├── workspace/              # inbox、正式项目和历史归档
├── var/                    # 可删除的运行时与临时产物
├── .codex/                 # Codex 本地 Skills
├── .venv-modeling/         # 本机 Python 建模环境，不纳入 Git
├── ENV_SETUP.md # 虚拟环境重建说明，由独立贡献者维护
├── AGENTS.md               # Agent 入口与强制路由
├── README.md               # 仓库入口
└── setup.bat               # Windows 环境引导脚本，由独立贡献者维护
```

完整职责和项目目录树见[工作区架构](docs/architecture/workspace-layout.md)，文档总索引见[文档中心](docs/README.md)。

## 快速入口

- [工作区治理规范](docs/standards/workspace-governance.md)
- [论文写作规范](docs/standards/paper-writing.md)
- [命名规范](docs/standards/naming.md)
- [建模环境指南](docs/guides/modeling-environment.md)
- [论文生产流程](docs/guides/paper-production.md)
- [算法资源库索引](resources/algorithm-library/index.md)
- [写作前强制学习流程](docs/guides/pre-writing-learning.md)
- [项目区](workspace/projects/README.md)
- [资源区](resources/README.md)

## 常用命令

```powershell
# 安装或同步建模依赖
.\.venv-modeling\Scripts\python.exe -m pip install -r config/python/requirements-modeling.txt

# 检查建模环境、依赖和外部工具
.\.venv-modeling\Scripts\python.exe tools/check-modeling-env.py

# 检查工作区层级、根目录白名单和命名
.\.venv-modeling\Scripts\python.exe tools/check-workspace-layout.py

# 创建标准项目
.\.venv-modeling\Scripts\python.exe .codex/skills/cumcm-paper-production/scripts/init_cumcm_project.py --root workspace/projects --contest cumcm --year 2026 --problem a
```

具体项目的计算、编译和审校命令必须记录在该项目的 `00-admin/runbook.md` 中。根目录不得放置项目脚本、论文、结果、临时文件或新增的专题文档。
