# 工作区架构与目录职责

本文档定义仓库级结构；项目内部结构由同一套约定继续约束。设计目标是让稳定文档、配置、工具和资源与频繁变化的项目数据、运行缓存分离。

## 设计原则（`LAYOUT-001`）

1. **根目录只做入口。** 根目录只保留 `README.md`、`AGENTS.md`、版本控制文件、隐藏环境目录和一级职责层。
2. **稳定资产与工作数据分离。** 规范、配置、工具和模板不与赛题项目混放。
3. **项目彼此隔离。** 每个正式需求只有一个项目目录，项目代码不得读取其他项目的隐式产物。
4. **原始数据受保护。** 具体不可变性和派生数据规则执行 `docs/standards/workspace-governance.md` 的 `WG-DATA-001`。
5. **运行时产物可删除。** 缓存、渲染页和调试输出统一进入 `var/tmp/`，不得成为唯一证据。

## 仓库目录树

```text
.
├── config/
│   └── python/
│       └── requirements-modeling.txt
├── docs/
│   ├── architecture/
│   ├── guides/
│   └── standards/
├── resources/
│   ├── algorithm-library/
│   ├── paper-library/
│   └── templates/
├── tools/
├── workspace/
│   ├── inbox/
│   ├── projects/
│   └── archive/
├── var/
│   └── tmp/
├── .codex/
├── .venv-modeling/
├── AGENTS.md
└── README.md
```

## 一级目录职责

| 路径 | 职责 | 允许内容 | 禁止内容 |
|---|---|---|---|
| `config/` | 工作区级配置 | 依赖锁定、静态配置 | 项目参数、运行结果 |
| `docs/` | 稳定文档 | 架构、规范、指南 | 赛题草稿、临时记录 |
| `resources/` | 只读或低频复用资产 | 算法说明、模板、优秀论文参考 | 当前项目代码、论文、正式引用台账 |
| `tools/` | 跨项目工具 | 环境自检、通用转换和审计辅助 | 单题模型代码 |
| `workspace/inbox/` | 新需求入口 | 尚未归类的需求和原始附件 | 长期项目成果 |
| `workspace/projects/` | 正式项目总库 | 独立、可复现的项目目录 | 跨项目共享工具 |
| `workspace/archive/` | 历史归档 | 停用版本和迁移快照 | 当前权威来源 |
| `var/tmp/` | 可删除运行时目录 | 缓存、渲染页、调试截图 | 唯一副本、原始数据、交付物 |
| `.codex/` | 本地自动化能力 | Skills、脚本和相关参考 | 赛题项目文件 |
| `.venv-modeling/` | 本机 Python 环境 | 解释器和已安装依赖 | 项目代码与数据 |

## 正式项目结构

正式项目路径固定为 `workspace/projects/<contest>-<year>-<problem>/`：

```text
<project-id>/
├── 00-admin/               # 清单、环境、运行手册、写作前学习记录和状态
├── 01-problem/             # 原题、附件清单和问题核对
├── 02-data/
│   ├── raw/                # 只读原始数据
│   └── processed/          # 可由程序再生的数据
├── 03-models/              # 模型选择记录、代码、算法、配置和参数
├── 04-results/
│   ├── figures/
│   ├── tables/
│   ├── metrics/
│   └── logs/
├── 05-evidence/            # 证据、文献和 AI 使用台账
├── 06-paper/
│   ├── figures/
│   └── tables/
├── 07-review/              # 自动审计、独立审校、论文质量与国奖竞争力审查记录
└── 08-delivery/            # 仅保留可提交成品
```

项目目录的工程门禁见 `docs/standards/workspace-governance.md`，证据字段见 `docs/standards/evidence-contract.md`，论文质量审查见 `docs/standards/paper-quality-audit.md`。本文件只定义位置和生命周期，不重复各规范的内容门禁。

## 需求生命周期

1. 在 `workspace/inbox/<yyyy-mm-dd>-<short-name>/` 保存新需求和附件。
2. 明确赛题后，用初始化脚本在 `workspace/projects/` 创建唯一项目。
3. 将原题和附件分别归入项目 `01-problem/`、`02-data/raw/`。
4. 清空对应 inbox 子目录，避免维护两份原始材料。
5. 项目不再活跃且确认无当前依赖后，才可移入 `workspace/archive/`。

## 放置决策

- 影响所有项目的规则或说明：`docs/`。
- 影响所有项目的固定配置：`config/`。
- 能跨项目执行的程序：`tools/`。
- 可复用但不直接执行的材料：`resources/`。
- 跨项目算法说明统一放 `resources/algorithm-library/`，优秀论文与阅读参考放 `resources/paper-library/`。
- 只服务某一道题的数据、代码或论文：对应项目目录。
- 随时可重新生成且无需保留的文件：`var/tmp/`。

任何无法归入上述类别的文件都不应直接留在根目录；先明确其生命周期和权威来源，再决定位置。

可在仓库根目录运行以下命令验证结构：

```powershell
.\.venv-modeling\Scripts\python.exe tools/check-workspace-layout.py
```
