# 数学建模工作区任务路由

先判断当前任务类型，只读取能直接约束该任务的文件。**禁止为普通局部任务预加载完整治理规范、完整 Production Skill 或其它无关长规范。** 跨阶段生产或最终审校任务才进入对应 Skill；单文件编辑、脚本诊断、一般问答只读取目标文件及其直接依赖。

> **路径约定：** 文档和 Skill 中的仓库路径均相对工作区根目录。要求绝对路径的工具调用必须先据当前根目录解析；Shell 仅在工作目录已明确设为仓库根目录时使用相对路径。

## 按任务加载

| 当前任务 | 必读权威文件 | 仅在触发时追加 |
|---|---|---|
| 仓库/项目目录位置与放置职责 | `docs/architecture/workspace-layout.md` | 涉及稳定命名时追加 `docs/standards/naming.md` |
| 文件名、项目 ID 与稳定标签 | `docs/standards/naming.md` | 涉及目录职责时才追加工作区架构 |
| 数据读取、清洗、环境、运行、日志、随机种子、复现 | `docs/standards/data-reproducibility.md` | 环境安装再读 `docs/guides/modeling-environment.md` |
| PDF 与 Excel 的读取、盘点、清洗 | `tools/README.md` | 需要运行环境或依赖时追加 `docs/guides/modeling-environment.md` |
| 模型选择、算法、代码实现、正式计算、验证 | `docs/standards/modeling-execution.md` | 先读 `resources/algorithm-library/index.md`，再只读匹配算法说明；涉及数据时追加数据复现规范 |
| 主张、数值或文献证据 | `docs/standards/evidence-contract.md` | 涉及跨阶段生命周期或交付时追加工作区治理规范 |
| inbox—project—archive 生命周期、产物地图、影响传播或 `sandbox/` 与正式链路边界 | `docs/standards/workspace-governance.md` 的 `WG-ROUTE-001`、`WG-TEST-001` | 涉及目录位置再读工作区架构；涉及实验比较再读建模执行规范 |
| AI 使用记录 | `docs/standards/workspace-governance.md` 的 `WG-AI-001` | 追加当前项目赛事 profile 的 `config/contests/<profile>/rules.md` 核对当届披露要求 |
| 论文内容、结构、建模叙事、结果分析、学术表达 | `docs/standards/paper-writing.md` | 启动正式写作时追加 `docs/guides/pre-writing-learning.md`；不要因纯排版任务加载它 |
| LaTeX、公式、表格、字体、页面与版式 | `docs/standards/paper-formatting.md` | 内容同时变化时才追加论文写作规范 |
| 论文图片、科研可视化、流程图或最终 PDF 图片检查 | `docs/standards/paper-figures.md` | 生成或改善视觉质量时追加 `docs/guides/scientific-figure-aesthetics.md` 和 `resources/figure-style-library/README.md`，只选少量相关参考 |
| 完整数学建模生产流程 | `.codex/skills/modeling-paper-production/SKILL.md` | 按 Skill 所列阶段加载对应权威文件 |
| 最终审校、评分或发布门禁 | `.codex/skills/modeling-paper-audit/SKILL.md`、`docs/standards/paper-quality-audit.md` | 按实际审校范围加载数据、模型、证据、写作、排版、图片和现行规则 |
| 当届规则、提交格式、AI 披露或匿名性 | 当前项目赛事 profile 的 `config/contests/<profile>/rules.md` | 正式提交前重新核对官网 |

职责不清时只查 `docs/README.md` 的唯一权威矩阵，不因此加载矩阵中的全部文件。适用门禁必须执行，但控制编号的完整定义只从其唯一权威文件读取；局部任务不得被无关阶段门禁扩张为全流程任务。

## 项目产物快速定位

任务需要定位正式项目上游产物、追踪变化或使用 `sandbox/` 时，加载 `WG-ROUTE-001` 与 `WG-TEST-001` 并按其步骤执行；本入口不复制地图字段、影响语义或实验产物边界。

## 全局约束

跨阶段优先级、证据路由、自动检查边界和临时产物治理只以 `docs/standards/workspace-governance.md` 为准；本入口只负责把任务路由到该权威文件。
