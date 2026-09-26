# 文档中心

每项规则只在一个权威文件中定义。`AGENTS.md` 只负责按任务路由；指南、Skill、模板和检查表只引用控制编号或权威文件，不复制阈值、字段、格式规则和判断标准。机器仅解析权威文件内显式的 `toml machine-contract` 块，不解析普通中文措辞或 Markdown 章节结构。

## 唯一权威职责矩阵

| 主题 | 唯一权威 | 其它文件的职责 |
|---|---|---|
| 仓库与项目目录职责、推荐骨架及 `sandbox/` 的空间位置 | `architecture/workspace-layout.md` | 入口导航、初始化器与结构检查执行 |
| 跨项目通用工具的使用与命令 | `tools/README.md` | 入口、Skill 与指南只引用，不复制用法 |
| 文件名、项目 ID 与稳定标签 | `standards/naming.md` | 初始化脚本执行命名 |
| 跨阶段优先级、项目生命周期、产物导航与影响传播、正式/实验产物边界、AI 路由、审校交接与交付治理 | `standards/workspace-governance.md` | 架构只给位置；生产与审校 Skill 编排；工具执行 machine contract |
| 原始数据、数据审计、环境、运行记录、日志、随机种子、稳定产物与复现 | `standards/data-reproducibility.md` | 建模流程调用，脚本执行；`WG-DATA-001` 在此定义 |
| 模型与算法选择、实现、正式计算、计算检查、性能记录与验证 | `standards/modeling-execution.md` | 算法库提供候选，生产/审校 Skill 执行；`WG-MODEL-001`、`PW-VAL-001` 在此定义 |
| 主张证据和文献台账文件、字段、状态与核验契约 | `standards/evidence-contract.md` | 治理规范规定生命周期，脚本校验字段；`WG-EVID-001` 在此定义 |
| 论文内容组织、结构、建模叙事、结果分析、学术表达、引用、附录内容与匿名性 | `standards/paper-writing.md` | 生产流程引用，质量审查判定 |
| LaTeX、页面、字体、字号、段落、公式、表格、单位、有效数字与纯版式 | `standards/paper-formatting.md` | 模板实现，生产与审校流程核验；`PW-FMT-001` 在此定义 |
| 论文图片与科研可视化的选择、生成、排版、导出和视觉审校 | `standards/paper-figures.md` | 生产与审校 Skill 执行；`PW-FIG-001` 在此定义 |
| 科研图片审美参考的选择、提取与使用方法 | `guides/scientific-figure-aesthetics.md` | 引用 `PW-FIG-001`，不另设阈值；样例资产由参考库承载 |
| 写作前学习流程与完成状态 | `guides/pre-writing-learning.md` | 其它文件只引用 `PWL-GATE-001` |
| Draft/RC/Final 审查生命周期、复查范围、硬错误边界、竞争力评分、报告字段和发布判定 | `standards/paper-quality-audit.md` | 治理规范只规定交接与路由；审校 Skill 执行；脚本只校验显式客观字段，不解析评分 |
| 当届赛事官方规则快照（按 profile） | `../config/contests/<profile>/rules.md` | Core 文档以"当前项目赛事官方基线"中性引用，由项目 `00-admin/project.yaml` 的 `contest`/`profile` 解析；提交前重新核对官网 |
| Agent 生产与审校步骤 | 对应 `.codex/skills/` | 编排权威规则，不重新定义规范参数 |
| 用户快速操作与命令 | `guides/paper-production.md` | 不重新定义门禁参数 |

## 架构

- [工作区架构与目录职责](architecture/workspace-layout.md)

## 规范

- [全局工作区治理](standards/workspace-governance.md)
- [数据与复现规范](standards/data-reproducibility.md)
- [建模与计算执行规范](standards/modeling-execution.md)
- [证据契约](standards/evidence-contract.md)
- [论文写作规范](standards/paper-writing.md)
- [论文排版规范](standards/paper-formatting.md)
- [论文图片与科研可视化规范](standards/paper-figures.md)
- [最终审查与竞争力评分标准](standards/paper-quality-audit.md)
- [命名与文件格式规范](standards/naming.md)

## 赛事 Profile

- [CUMCM 现行官方规则基线](../config/contests/cumcm/rules.md)
- [MCM/ICM 现行官方规则基线](../config/contests/mcm-icm/rules.md)：`mcm` 与 `icm` 共用此 profile；新增赛事在 `config/contests/` 下新建 profile 目录并配 `profile.yaml`。

## 指南

- [建模环境指南](guides/modeling-environment.md)
- [论文生产流程](guides/paper-production.md)
- [写作前强制学习流程](guides/pre-writing-learning.md)
- [科研图片审美参考使用指南](guides/scientific-figure-aesthetics.md)

## 跨项目资源入口

- [算法资源库索引](../resources/algorithm-library/index.md)
- [优质论文参考库](../resources/paper-library/README.md)
- [科研图片风格参考库](../resources/figure-style-library/README.md)

新增稳定文档时必须先在矩阵中确定唯一职责，再归入相应类别；不得在入口、Skill、指南或模板中建立第二套规则。具体项目的运行手册、分析记录和论文说明留在相应项目内。
