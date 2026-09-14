# 数学建模工作区任务路由

先判断当前任务类型，只读取能直接约束该任务的文件。**禁止为普通局部任务预加载完整治理规范、完整 Production Skill 或其它无关长规范。** 跨阶段生产或最终审校任务才进入对应 Skill；单文件编辑、脚本诊断、一般问答只读取目标文件及其直接依赖。

> **路径约定：** 文档和 Skill 中的仓库路径均相对工作区根目录。要求绝对路径的工具调用必须先据当前根目录解析；Shell 仅在工作目录已明确设为仓库根目录时使用相对路径。

## 按任务加载

| 当前任务 | 必读权威文件 | 仅在触发时追加 |
|---|---|---|
| 目录、inbox 与文件路由 | `docs/architecture/workspace-layout.md` | 涉及稳定命名时追加 `docs/standards/naming.md`；跨阶段治理再追加全局治理规范 |
| 文件名、项目 ID 与稳定标签 | `docs/standards/naming.md` | 涉及目录职责时才追加工作区架构 |
| 数据读取、清洗、环境、运行、日志、随机种子、复现 | `docs/standards/data-reproducibility.md` | 环境安装再读 `docs/guides/modeling-environment.md` |
| 模型选择、算法、代码实现、正式计算、验证 | `docs/standards/modeling-execution.md` | 先读 `resources/algorithm-library/index.md`，再只读匹配算法说明；涉及数据时追加数据复现规范 |
| 主张、数值或文献证据 | `docs/standards/evidence-contract.md` | 涉及跨阶段生命周期或交付时追加工作区治理规范 |
| AI 使用记录 | `docs/standards/workspace-governance.md` 的 `WG-AI-001` | 追加 `docs/standards/cumcm-current-rules.md` 核对当届披露要求 |
| 论文内容、结构、建模叙事、结果分析、学术表达 | `docs/standards/paper-writing.md` | 启动正式写作时追加 `docs/guides/pre-writing-learning.md`；不要因纯排版任务加载它 |
| LaTeX、公式、表格、字体、页面与版式 | `docs/standards/paper-formatting.md` | 内容同时变化时才追加论文写作规范 |
| 论文图片、科研可视化、流程图或最终 PDF 图片检查 | `docs/standards/paper-figures.md` | 生成或改善视觉质量时追加 `docs/guides/scientific-figure-aesthetics.md` 和 `resources/figure-style-library/README.md`，只选少量相关参考 |
| 完整数学建模生产流程 | `.codex/skills/cumcm-paper-production/SKILL.md` | 按 Skill 所列阶段加载对应权威文件 |
| 最终审校、评分或发布门禁 | `.codex/skills/cumcm-paper-audit/SKILL.md`、`docs/standards/paper-quality-audit.md` | 按实际审校范围加载数据、模型、证据、写作、排版、图片和现行规则 |
| 当届规则、提交格式、AI 披露或匿名性 | `docs/standards/cumcm-current-rules.md` | 正式提交前重新核对官网 |

职责不清时只查 `docs/README.md` 的唯一权威矩阵，不因此加载矩阵中的全部文件。适用门禁必须执行，但控制编号的完整定义只从其唯一权威文件读取；局部任务不得被无关阶段门禁扩张为全流程任务。

## 项目产物快速定位

任务已落到某个正式项目，且需要读取上游产物时，先打开该项目的 `00-admin/artifact-map.yaml`：只沿 `common` 和当前 `question_id` 中与任务相关的路径读取数据、代码、参数、正式结果和验证产物；证据 ID 再到地图所指向的证据台账解析。不要把“定位产物”默认实现为扫描完整项目树。

产物地图只是导航索引，不替代题面清单、运行手册、模型选择记录、证据台账或各主题权威规范。创建、移动或淘汰一个会被下游复用的稳定关键产物时，顺手更新受影响条目；临时文件、缓存、探索候选、每个辅助脚本、哈希和阶段状态不登记。旧项目缺少地图或条目已经失效时，只在相关职责目录做一次定向搜索，并修复本次实际用到的关键路径，不要求补录整个项目历史。

已登记的上游数据、代码、参数、结果或验证产物发生实质变化后，在复用下游内容前运行 `tools/trace-artifact-impact.py` 并显式传入变化路径。`STALE` 项重新生成，`RECHECK` 项依据新结果核对后再决定是否更新；该只读分析不写状态、不替代证据核验或 Final Audit，也不因普通措辞修改触发模型重跑。跨子问题依赖只在地图的 `depends_on_questions` 中登记实际存在的例外关系。

正式项目的 `test/` 是编号阶段之外的可选实验沙盒。模型选择前可用它做小规模候选比较，正式模型建立后可先在其中验证局部改动；其中产物不得登记到产物地图、证据台账或直接进入论文/交付。只有确认采纳并在 `03-models/`、`04-results/` 等正式路径重新实现、运行和验证后，才对这些正式变化执行影响追踪。

## 全局约束

- 当届官方规则和用户当前明确要求优先。
- 数值、验证、文献、AI 使用和审校结论必须有可核验证据，不得以聊天记忆、作者自述或未保存输出替代。
- 不得因重构、精简或自动检查而删除、放宽或复制权威规则；机器只阻断高风险、客观、稳定且可自动判断的问题。
- 临时产物进入 `var/temp/`；项目数据、模型代码和运行产物不得散落仓库根目录。
