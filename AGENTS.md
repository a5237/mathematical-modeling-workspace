# 数学建模工作区 Agent 入口

本仓库采用分层工程结构。涉及数学建模竞赛的分析、代码、论文、审校或交付任务时，必须先读取：

> **Agent 工具路径约定：** 本文件及各 Skill 中反引号标注的仓库文件路径均为相对于当前工作区根目录的逻辑路径。调用要求绝对路径的文件读取、查看或编辑工具前，必须先用该工具可识别的当前工作区根目录解析为绝对路径；不得把 `docs/...`、`.codex/...` 等相对路径原样传入，也不得猜测为 `/docs/...` 或 `/.codex/...`。Shell 命令只有在工作目录已明确设置为仓库根目录时才可直接使用这些相对路径。该约定仅约束 Agent 的工具调用，不改变项目代码优先使用相对路径或项目根解析的可复现要求。

1. `docs/standards/workspace-governance.md`；
2. `.codex/skills/cumcm-paper-production/SKILL.md`；
3. 涉及模型建立或代码编写时，先读取 `resources/algorithm-library/index.md`，再只读取与当前问题匹配的算法说明；
4. 涉及论文内容、排版或附录时，再读取 `docs/standards/paper-writing.md` 和 `docs/guides/pre-writing-learning.md`；
5. 涉及论文图片、科研可视化、流程图、结构图或最终 PDF 图片检查时，再读取 `docs/standards/paper-figures.md`；
6. 涉及最终审校时，再读取 `.codex/skills/cumcm-paper-audit/SKILL.md` 和 `docs/standards/paper-quality-audit.md`；
7. 涉及当届规则、提交格式、AI 披露或匿名性时，读取 `docs/standards/cumcm-current-rules.md` 并在正式提交前重新核对官网。

各文档的唯一权威职责见 `docs/README.md`。工作区规范负责环境、数据、代码、日志、证据、复现和交付；目录职责、命名、论文写作、论文图片、学习流程、官方规则和质量审查分别由矩阵指定文件管理。工程记录不得因工作区要求而自动写入论文正文。

## 全局质量门禁

- 必须执行 `WG-DATA-001`、`WG-MODEL-001`、`WG-EVID-001`、`PWL-GATE-001`、`PW-VAL-001`、`PW-FIG-001` 与 `PQA-RELEASE-001`；控制编号对应的完整规则只以权威文件为准。
- 任何数值、验证、文献、AI 使用和审校结论都必须有权威记录或可核验证据，不得用聊天记忆、作者自述或未保存输出替代。
- 重构、拆分或精简规范时，不得删除、放宽或绕过论文结构、论证、验证、图表、文献、公式、排版、匿名性和交付门禁；只允许迁移到职责明确的唯一权威文件。
- 当届官方规则和用户当前明确要求优先；正式提交前必须重新核对全国组委会官网。

项目目录和文件命名遵循 `docs/standards/naming.md`。新项目优先使用生产 Skill 的初始化脚本创建。

## 工作区文件路由（强制）

全部目录职责和需求生命周期以 `docs/architecture/workspace-layout.md` 为唯一权威，文件名与稳定标识以 `docs/standards/naming.md` 为唯一权威。新需求先进入规定的 inbox，正式项目使用标准项目树，临时产物进入 `var/tmp/`，仓库根目录不得新增专题文档或项目产物。环境准备见 `docs/guides/modeling-environment.md`。
