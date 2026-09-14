# 工作区架构与目录职责

本文档是 Agent 组织仓库与项目文件的权威指南。设计目标是让稳定文档、配置、工具和资源与频繁变化的项目数据、运行缓存分离；下列目录树是推荐基线，不是由 Python 精确复刻的固定 schema。

## 设计原则（`LAYOUT-001`）

1. **根目录主要做入口。** 常用入口仍为 `README.md`、`AGENTS.md`、`ENV_SETUP.md`、`setup.bat`、版本控制文件、隐藏环境目录和一级职责层；合理新增顶层入口或职责目录不会仅因不在旧清单中而失败。环境规则仍以 `docs/guides/modeling-environment.md` 为准。
2. **稳定资产与工作数据分离。** 规范、配置、工具和模板不与赛题项目混放。
3. **项目彼此隔离。** 每个正式需求只有一个项目目录，项目代码不得读取其他项目的隐式产物。
4. **原始数据受保护。** 具体不可变性和派生数据规则执行 `docs/standards/data-reproducibility.md` 的 `WG-DATA-001`。
5. **运行时产物可删除。** 缓存、PDF 页面截取、渲染页和调试输出统一进入 `var/temp/`，不得成为唯一证据。布局机器检查只拦截明显缓存/生成污染、批量项目产物散落和会造成冲突的废弃结构，不检查普通命名与完整目录存在性。

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
│   ├── figure-style-library/
│   ├── paper-library/
│   └── templates/
├── tools/
├── workspace/
│   ├── inbox/
│   ├── projects/
│   └── archive/
├── var/
│   └── temp/
├── .codex/
├── .venv-modeling/
├── AGENTS.md
├── ENV_SETUP.md
├── README.md
└── setup.bat
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
| `var/temp/` | 可删除运行时目录 | 缓存、PDF 页面截取、渲染页、调试截图 | 唯一副本、原始数据、交付物 |
| `.codex/` | 本地自动化能力 | Skills、脚本和相关参考 | 赛题项目文件 |
| `.venv-modeling/` | 本机 Python 环境 | 解释器和已安装依赖 | 项目代码与数据 |

## 正式项目结构

正式项目通常位于 `workspace/projects/<project-id>/`，其中 `<project-id>` 按 `docs/standards/naming.md` 生成。初始化器创建以下推荐骨架：

```text
<project-id>/
├── 00-admin/               # 清单、环境、运行手册、产物导航、写作学习与选图决策记录和状态
│   └── artifact-map.yaml   # 按子问题定位稳定关键产物的轻量入口
├── 01-problem/             # 原题、附件清单和问题核对
│   └── attachments/        # 不属于原始数据表的题面附件
├── 02-data/
│   ├── raw/                # 只读原始数据
│   └── processed/          # 可由程序再生的数据
├── 03-models/              # 模型选择记录、代码、算法、配置和参数
│   └── q01/                # 初始化示例，可按实际子问题或模型重构
├── 04-results/
│   ├── figures/
│   ├── tables/
│   ├── metrics/
│   └── logs/
├── 05-evidence/            # 证据、文献和 AI 使用台账
├── 06-paper/
│   ├── figures/
│   └── tables/
├── 07-review/              # 审稿记录与 RC/Final 唯一最终审查报告
├── 08-delivery/            # 仅保留可提交成品
│   └── support-materials/  # 当届要求的可运行代码与支撑材料
└── test/                   # 可由任一阶段调用的轻量实验沙盒，不属于线性阶段
```

除保留名称 `test/` 的特殊职责外，项目可根据题目增加、拆分或重构其它内部目录，例如 `benchmarks/`、`simulations/` 或按模型组织的子树。只要原始数据保护、权威模型/参数、机器结果、证据、论文与交付关系仍明确且可复现，这些变化不构成审查错误。初始化骨架负责提供可靠起点，不限制项目后续演化。

### `test/` 实验区

`test/` 与 `00-admin/` 至 `08-delivery/` 并列，但不是第 09 阶段，也不改变正式阶段的先后关系或门禁。各阶段可按需用它做小样本、小规模、短时运行的候选算法、参数和局部实现比较，以便在修改正式链路前先验证想法。

- 初始化器只创建 `test/README.md`，不复制正式工作流目录树。需要实验时可在 `test/` 下按问题或想法临时组织代码、数据、结果和简短结论，无需维护统一子目录、完整运行手册、证据台账或阶段状态。
- `test/` 内全部内容默认属于 exploratory 非权威产物。不得把其中的代码、数据、指标、图片、表格或日志登记到 `00-admin/artifact-map.yaml`，也不得直接作为 `04-results/` 的正式结果、`05-evidence/` 的证据、`06-paper/` 的引用来源或 `08-delivery/` 的交付物。
- 实验被采纳后，须在 `03-models/` 中形成正式实现和参数，按正式数据与复现规则运行到 `04-results/`，完成适用验证并登记证据；只有这些正式路径进入产物地图和后续影响链。未采纳实验可保留或删除，不触发正式链路重跑。
- `test/` 不豁免、替代或降低任何正式工作流门禁。正式结果仍以编号阶段中的权威产物为准。

### 项目产物导航

每个新初始化的正式项目包含 `00-admin/artifact-map.yaml`。它按 `common` 与 `q01`、`q02` 等稳定子问题 ID，列出下游阶段需要再次读取的关键数据、代码入口、参数、正式结果、验证产物和论文引用副本；证据部分只登记 `claim_id` 或 `citation_key`，具体来源与核验状态仍由 `05-evidence/` 台账管理。

地图中的 `impact_defaults` 只保存一次通用类别依赖：数据、代码或参数影响结果，结果影响验证与论文图表副本，结果和验证要求重新核对证据、论文、审校与交付。`paper_assets` 专指 `06-paper/figures/`、`06-paper/tables/` 中从权威结果复制或导出的文件。只有一个子问题实际依赖另一问的产物时，才在该问的 `depends_on_questions` 中登记 `<question_id>.<category>`；其语义是该上游类别变化会使本问结果进入影响链。

发生实质变化后可运行：

```powershell
.\.venv-modeling\Scripts\python.exe tools/trace-artifact-impact.py `
  workspace/projects/<project-id> `
  --changed 02-data/processed/q01-data.csv 03-models/q01/q01-parameters.yaml
```

工具只读取地图和显式变化路径并计算传递影响：`STALE` 表示列出的派生产物必须重新生成，`RECHECK` 表示证据主张、正文、审校结论或交付件需结合新结果核对，核对后确认未受影响的内容可继续复用。它不自动读取 Git diff，不写入动态失效状态，返回影响项也不等于新增发布门禁。地图缺失或路径未登记时，工具只按项目职责目录和路径中的 `qNN` 做保守推断并给出警告。

该文件是导航索引，不是完整 manifest，也不是新的权威数据源或阶段门禁：

- 只登记相对项目根目录的稳定关键文件，通常是运行入口和下游会引用的产物，不登记每个辅助脚本或中间文件；
- 不登记临时预览、缓存、失败输出、文件哈希、存在状态和阶段完成状态；
- 创建、移动或淘汰下游会复用的关键产物时，只更新受影响的 `common` 或子问题条目；
- 通用影响关系不逐问复制，跨问依赖只登记实际例外；不维护逐次变更日志或动态失效清单；
- Agent 进入论文写作、结果分析、制图或审校时先读取该地图，再按当前子问题定向打开文件；地图缺失或失效时只搜索相关职责目录，并修复本次实际使用的关键路径；
- 旧项目缺少地图不自动构成发布阻断，审校也不得把地图条目本身当作主张、验证或复现证据。

项目生命周期与交付治理见 `docs/standards/workspace-governance.md`，数据复现与建模执行分别见 `docs/standards/data-reproducibility.md` 和 `docs/standards/modeling-execution.md`，证据字段见 `docs/standards/evidence-contract.md`，论文质量审查见 `docs/standards/paper-quality-audit.md`。本文件不要求审计脚本复制完整目录树。

## 需求生命周期

1. 在 `workspace/inbox/<yyyy-mm-dd>-<short-name>/` 保存题目要求、用户说明和原始附件；该命名是推荐约定，不是独立机器门禁。
2. 明确赛题后，用初始化脚本在 `workspace/projects/` 创建唯一项目。
3. 将原题和附件分别归入项目 `01-problem/`、`02-data/raw/`。
4. 清空对应 inbox 子目录，避免维护两份原始材料。
5. 项目不再活跃且确认无当前依赖后，才可移入 `workspace/archive/`。

## 放置决策

- 影响所有项目的规则或说明：`docs/`。
- 影响所有项目的固定配置：`config/`。
- 能跨项目执行的程序：`tools/`。
- 可复用但不直接执行的材料：`resources/`。
- 跨项目算法说明统一放 `resources/algorithm-library/`，科研图片审美锚点放 `resources/figure-style-library/`，优秀论文与阅读参考放 `resources/paper-library/`。
- 只服务某一道题的数据、代码或论文：对应项目目录。
- 随时可重新生成且无需保留的文件：`var/temp/`。

任何无法归入上述类别的文件都应先明确生命周期和权威来源，再决定位置。单个合理的新入口不会被机器直接判错，但项目数据、模型代码、缓存和生成产物仍应路由到对应项目或 `var/temp/`。

可在仓库根目录运行以下命令捕获高风险污染；该命令不验证完整目录树或普通命名：

```powershell
.\.venv-modeling\Scripts\python.exe tools/check-workspace-layout.py
```
