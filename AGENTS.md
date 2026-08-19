# 数学建模工作区 Agent 入口

本仓库采用分层工程结构。涉及数学建模竞赛的分析、代码、论文、审校或交付任务时，必须先读取：

> **Agent 工具路径约定：** 本文件及各 Skill 中反引号标注的仓库文件路径均为相对于当前工作区根目录的逻辑路径。调用要求绝对路径的文件读取、查看或编辑工具前，必须先用该工具可识别的当前工作区根目录解析为绝对路径；不得把 `docs/...`、`.codex/...` 等相对路径原样传入，也不得猜测为 `/docs/...` 或 `/.codex/...`。Shell 命令只有在工作目录已明确设置为仓库根目录时才可直接使用这些相对路径。该约定仅约束 Agent 的工具调用，不改变项目代码优先使用相对路径或项目根解析的可复现要求。

1. `docs/standards/workspace-governance.md`；
2. `.codex/skills/cumcm-paper-production/SKILL.md`；
3. 涉及模型建立或代码编写时，先读取 `resources/algorithm-library/index.md`，再只读取与当前问题匹配的算法说明；
4. 涉及论文内容、排版或附录时，再读取 `docs/standards/paper-writing.md` 和 `docs/guides/pre-writing-learning.md`；
5. 涉及最终审校时，再读取 `.codex/skills/cumcm-paper-audit/SKILL.md` 和 `docs/standards/paper-quality-audit.md`。

工作区规范负责目录、环境、版本、入口、日志、证据、复现和交付；论文写作规范只负责评审可见的论文内容与版式。工程记录不得因工作区要求而自动写入论文正文。

## 全局质量门禁

- 原始数据只读，不覆盖项目内 `02-data/raw/`。
- 具体数值只能来自已保存、可复现的程序输出。
- 灵敏度、误差和检验结论必须有对应运行产物。
- 文献只有在实际检索并登记后才能引用。
- 建模和编码前必须完成 `03-models/model-selection.md`；资源库中存在适用算法时优先采用，库外算法必须记录偏离理由和验证方案。
- 每个子问题最多两个独立主模型体系；同一物理机制的不同精度展开按一个模型族计数，基准、消融和验证对照不计入主模型数量。
- 正式写作前必须按 `docs/guides/pre-writing-learning.md` 阅读至少 2 篇同类优秀论文和相关算法资料，并完成 `00-admin/pre-writing-learning.md`。
- 每个论文主张必须能在证据索引中追溯到数据、代码、日志、表格、图或文献。
- 写作与终审分离，发布前必须运行独立审校。
- 竞赛规则可能变化，提交前以全国组委会官网最新文件为准。
- 任何身份信息不得进入提交论文、代码注释、元数据或支撑材料。
- 标题、摘要正文和关键词共同独占一页，正文从下一页开始；每个附录或附件必须单独新起一页。
- 摘要中的核心模型、关键数值、最终方案和结论性短语必须加粗。
- 全部中文（含标题、图表、页眉页脚和附录）使用宋体，全部英文字符和阿拉伯数字使用 Times New Roman。
- 每个子问题必须有集中列示的模型汇总公式；优化模型先列目标函数，下一行以 `s.t.` 集中列出约束。
- 参考文献原则上不少于 6 篇；《数学模型（第五版）》与《数学建模算法与应用》必须列入并在正文实际引用，其余至少 4 篇须与题目直接相关。
- 重构、拆分或精简规范时，不得删除或降低论文结构、论证、验证、图表、文献、公式和排版质量门禁；只能迁移职责明确属于工作区工程管理的内容。
- 发布前必须渲染逐页检查分页，并检查最终 PDF 的字体属性，不能只核对源文件。
- `07-review/` 必须包含论文质量审查；审查须分别判定 `paper-writing.md` 硬性合规与国奖竞争力，并逐图确认清晰、直观、无重叠、遮挡和歧义。

项目目录和文件命名遵循 `docs/standards/naming.md`。新项目优先使用生产 Skill 的初始化脚本创建。

## 工作区文件路由（强制）

- 新收到、尚未归类的需求与附件只放 `workspace/inbox/<yyyy-mm-dd>-<short-name>/`；完成归类后不得长期滞留。
- 正式项目只放 `workspace/projects/<contest>-<year>-<problem>/`，并使用 `00-admin` 至 `08-delivery` 的标准目录。
- 原题放项目 `01-problem/`；原始数据只放 `02-data/raw/` 且保持只读；清洗数据只放 `02-data/processed/`。
- 可运行代码、参数与算法实现只放 `03-models/`；不得把项目代码散落在仓库根目录。
- 程序生成的图片、表格、指标和日志只放 `04-results/figures|tables|metrics|logs/`；论文引用副本放 `06-paper/figures|tables/`。
- 论文源文件只放 `06-paper/`；自动审计、发布审校和论文质量审查记录只放 `07-review/`；可提交成品只放 `08-delivery/`。
- 优质论文只放 `resources/paper-library/`；通用模板只放 `resources/templates/`；跨项目工具只放 `tools/`。
- 跨项目算法说明只放 `resources/algorithm-library/`；资源库示例不得替代项目 `03-models/` 中的正式代码和真实运行产物。
- 临时渲染、缓存和调试截图只放 `var/tmp/`，任务结束必须清理；历史旧结构只放 `workspace/archive/`，禁止作为当前权威来源。
- 工作区级依赖和配置只放 `config/`；规范、架构和指南只放 `docs/`。
- 仓库根目录只保留入口文件和系统目录，不新增专题 Markdown、依赖清单、项目产物或临时文件。

详细目录职责见 `docs/architecture/workspace-layout.md`，环境准备见 `docs/guides/modeling-environment.md`。
