# 文档中心

工作区文档按职责分为三类。每项规则只在一个权威文件中定义；入口、指南、Skill、检查表和脚本可以引用或执行规则，但不得维护第二套阈值、数量或字段定义。

## 权威职责矩阵

| 主题 | 唯一权威 | 其它文件的职责 |
|---|---|---|
| 仓库与项目目录职责 | `architecture/workspace-layout.md` | 入口导航、结构检查 |
| 文件名、项目 ID 与稳定标签 | `standards/naming.md` | 初始化脚本执行命名 |
| 数据、代码、环境、复现、产物和交付工程门禁 | `standards/workspace-governance.md` | 生产 Skill 执行，审校 Skill 核验 |
| 主张证据和文献台账字段 | `standards/evidence-contract.md` | 治理规范规定路由，脚本校验字段 |
| 论文内容、结构、公式、图表、字体和文献组成 | `standards/paper-writing.md` | 生产流程引用，质量审查判定 |
| 写作前学习流程与完成状态 | `guides/pre-writing-learning.md` | 其它文件只引用 `PWL-GATE-001` |
| 论文质量、竞争力评分和审查报告模式 | `standards/paper-quality-audit.md` | 审校 Skill 执行，脚本校验机器字段 |
| 当届全国组委会规则快照 | `standards/cumcm-current-rules.md` | 提交前重新核对官网 |
| Agent 生产与审校步骤 | 对应 `.codex/skills/` | 不重新定义规范参数 |
| 用户快速操作与命令 | `guides/paper-production.md` | 不重新定义门禁参数 |

## 架构

- [工作区架构与目录职责](architecture/workspace-layout.md)

## 规范

- [工作区治理规范](standards/workspace-governance.md)
- [证据契约](standards/evidence-contract.md)
- [论文写作规范](standards/paper-writing.md)
- [论文质量审查标准](standards/paper-quality-audit.md)
- [CUMCM 现行官方规则基线](standards/cumcm-current-rules.md)
- [命名与文件格式规范](standards/naming.md)

## 指南

- [建模环境指南](guides/modeling-environment.md)
- [论文生产流程](guides/paper-production.md)
- [写作前强制学习流程](guides/pre-writing-learning.md)

## 跨项目资源入口

- [算法资源库索引](../resources/algorithm-library/index.md)
- [优质论文参考库](../resources/paper-library/README.md)

新增稳定文档时必须归入上述类别，不得直接放在仓库根目录。具体项目的运行手册、分析记录和论文说明应留在相应项目内。
