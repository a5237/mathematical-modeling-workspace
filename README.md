# 全国大学生数学建模工作区

这是一个面向长期复用的数学建模工作区。仓库按“文档、配置、工具、资源、工作数据、运行时产物”分层，正式赛题仍在各自项目内使用 `00-admin` 至 `08-delivery` 的可复现生产结构。

## 目录

- [快速上手工作区](#快速上手工作区)
- [仓库分层](#仓库分层)
- [关键文件说明](#关键文件说明)
- [常用命令](#常用命令)
- [快速入口](#快速入口)
- [接下来做什么？](#接下来做什么)
  - [如果你是人类](#如果你是人类)
  - [如果你是 Agent](#如果你是-agent)
- [进阶篇](#进阶篇)
  - [这套工作区是怎么设计的](#这套工作区是怎么设计的)
  - [人机协作](#人机协作)
- [最后提醒](#最后提醒)

## 快速上手工作区

如何开启你的第一次建模?请跟着以下步骤快速进行。

### 第1步:搭建 Python 环境

在项目根目录双击`setup.bat`(或在 PowerShell 中执行 `.\setup.bat`)。

这个脚本会自动:
- 检测你电脑上的 Python 版本(3.10 ~ 3.13)
- 创建虚拟环境 `.venv-modeling/`
- 安装 `config/python/requirements-modeling.txt` 中列出的所有依赖
- 检查 LaTeX 环境(`xelatex`)是否可用

> 如果提示“找不到 Python”，请先安装 Python 3.10 ~ 3.13 中的任一版本，并确保 `py` 启动器可用。

### 第2步:了解项目结构

```text

config/          → 依赖清单(一般不用动)
docs/            → 所有规范和指南(遇到问题先翻这里)
resources/       → 算法资料、优秀论文、模板(写作前可以翻翻)
tools/           → 辅助工具脚本(需要时可以调用)
workspace/       → 你的工作区
  ├── inbox/     → 新赛题暂存(放题目、附件的临时位置)
  ├── projects/  → 正式赛题项目(每一道题一个独立目录)
  └── archive/   → 历史归档(不再使用的旧项目)
  
```

### 第3步:开始你的第一道赛题

1. 将原始赛题 PDF 和附件放入 `workspace/inbox/` 
2. 在 Codex / Claude Code / DeepSeek Harness 中启动 Agent，提示词指向该inbox目录
3. Agent 会先读取轻量的 `AGENTS.md`，再按当前阶段只加载数据、建模、证据、写作、排版、图片或审校所需规范
4. 人类在 Day 3-4 介入审校和交付检查

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
├── ENV_SETUP.md 		   # 虚拟环境重建说明，由独立贡献者维护
├── AGENTS.md               # Agent 轻量任务路由入口
├── README.md               # 仓库入口
└── setup.bat               # Windows 环境引导脚本，由独立贡献者维护
```

完整职责和项目目录树见[工作区架构](docs/architecture/workspace-layout.md)，文档总索引见[文档中心](docs/README.md)。

## 关键文件说明

| 文件 | 用途 | 什么时候用 |
| :--- | :--- | :--- |
| `setup.bat` | 一键搭建 Python 虚拟环境 + 安装依赖 | 首次使用，或环境损坏时 |
| `tools/update.bat` | 增量补全缺失的依赖(不重建环境) | `requirements-modeling.txt` 更新后，或发现缺包时 |
| `tools/check-modeling-env.py` | 检查 Python 环境、依赖和外部工具 | 怀疑环境有问题时 |
| `tools/check-workspace-layout.py` | 捕获根目录高风险缓存、生成残留、批量项目产物和冲突旧结构 | 日常维护或重构后检查 |
| `tools/extract-spreadsheet.py` | 清洗 Excel 附件并逐工作表输出标准 CSV，也支持大表流式检查/提取 | 收到 `.xlsx/.xls` 题目附件时 |
| `tools/extract-pdf-pages.py` | 截取 PDF 指定页或页面局部并输出临时 PDF/PNG | 题面视觉分析、OCR 或临时引用时 |
| `tools/trace-artifact-impact.py` | 从显式变化路径计算项目产物的传递影响 | 修改上游后判断哪些结果必须重生成、哪些下游内容只需复核 |
| `AGENTS.md` | Agent 的按需加载路由与全局底线 | 如果你用 Codex/Claude Code 等 AI 工具 |
| `ENV_SETUP.md` | 虚拟环境的手动搭建步骤 | `setup.bat` 失效时需要 |


## 常用命令

### 环境准备(首次使用)

```powershell

# 一键搭建完整 Python 虚拟环境
.\setup.bat

```

### 日常开发与维护

```powershell

# 同步/补全依赖(当 config/python/requirements-modeling.txt 更新后执行)
.\tools\update.bat

# 检查建模环境、依赖和外部工具
.\.venv-modeling\Scripts\python.exe tools/check-modeling-env.py

# 检查根目录高风险污染（不冻结顶层结构或普通命名）
.\.venv-modeling\Scripts\python.exe tools/check-workspace-layout.py

```

### 项目初始化(启动新赛题)

```powershell
# 创建标准项目(以 2026 年 A 题为例)
.\.venv-modeling\Scripts\python.exe .codex/skills/cumcm-paper-production/scripts/init_cumcm_project.py --root workspace/projects --contest cumcm --year 2026 --problem a

```


## 快速入口

| 你想了解什么 | 去哪看 |
| :--- | :--- |
| 工作区整体架构 | [工作区架构](docs/architecture/workspace-layout.md) |
| 文件怎么放、目录怎么用 | [工作区架构](docs/architecture/workspace-layout.md) 与 [全局治理](docs/standards/workspace-governance.md) |
| 数据、运行和复现怎么做 | [数据与复现规范](docs/standards/data-reproducibility.md) |
| 模型、计算和验证怎么做 | [建模与计算执行规范](docs/standards/modeling-execution.md) |
| 证据怎么追溯 | [证据契约](docs/standards/evidence-contract.md) |
| 论文内容怎么写 | [论文写作规范](docs/standards/paper-writing.md) |
| LaTeX、公式、表格和版式怎么做 | [论文排版规范](docs/standards/paper-formatting.md) |
| 论文配图怎么做 | [论文图片与科研可视化规范](docs/standards/paper-figures.md) |
| 论文怎么审、何时复查 | [最终审查与竞争力评分标准](docs/standards/paper-quality-audit.md) |
| 怎么命名文件和项目 | [命名规范](docs/standards/naming.md) |
| 下游阶段怎么快速找到项目产物 | 正式项目的 `00-admin/artifact-map.yaml` |
| 上游修改后哪些产物受影响 | `tools/trace-artifact-impact.py` |
| 环境怎么配 | [建模环境指南](docs/guides/modeling-environment.md) |
| 论文生产流程是什么 | [论文生产流程](docs/guides/paper-production.md) |
| 写作前要做什么 | [写作前强制学习流程](docs/guides/pre-writing-learning.md) |
| 有什么算法可以参考 | [算法资源库索引](resources/algorithm-library/index.md) |
| 有什么模板可以用 | [资源区](resources/README.md) |
| 项目区在哪 | [项目区](workspace/projects/README.md) |

## 接下来做什么？

### 如果你是人类

1. 跑完 `setup.bat`，确认环境正常
2. 把新赛题的材料放入 `workspace/inbox/`
3. 按 `00-admin` → `01-problem` → ... → `08-delivery` 的顺序推进
   - Day 1-2：关注建模和代码(人类定方向，Agent 执行)
   - Day 3-4：关注审校和交付(Agent 生成草稿，人类检查逻辑、图表、排版、字体)

> 如果你希望在 Day 1 进行更深入的预建模研究，可以参考进阶篇的[人机协作](#人机协作)。

#### 论文审校与交付

Agent 生成 Release Candidate 后，应依据[最终审查标准](docs/standards/paper-quality-audit.md)完成证据、复现、内容一致性、排版、图表和最终 PDF 渲染检查，并提交可追溯的审查结果。具体要求分别以[论文写作规范](docs/standards/paper-writing.md)、[论文排版规范](docs/standards/paper-formatting.md)和[论文图片规范](docs/standards/paper-figures.md)为准，人类无需重复执行这些规范化检查。

人类审校重点放在规范难以穷尽的高层质量判断：

- **消除 AI 味和工程化语言**：删除写作过程、程序实现、配置管理和任务执行式表述，修正模板化开头、机械过渡、空泛评价、重复总结及过度分点，使论文呈现为自然、凝练的数学论证，而不是 Agent 工作报告。
- **判断获奖竞争力**：检查论文是否抓住题目核心矛盾，模型是否具有实质洞察而非方法堆砌，各问是否形成递进关系，结果是否鲜明、可信且具有应用价值。
- **把握论证重点和阅读体验**：从评阅者视角判断摘要能否迅速传达亮点，正文主线是否突出，关键发现是否得到充分解释，次要技术细节是否喧宾夺主。
- **确认团队真正理解论文**：检查模型选择、关键假设、结果含义和局限是否经得起追问，避免保留虽符合形式规范但团队无法解释或辩护的内容。

最终交付不是再次人工核对格式清单，而是在 Agent 完成规范审查的基础上，由人类对论文的自然表达、学术判断、实质亮点和竞赛说服力作最后把关。

### 如果你是 Agent

请先阅读 [`AGENTS.md`](AGENTS.md)。它只提供轻量任务路由和全局底线；随后按当前任务读取对应的唯一权威文件，不要预加载无关长规范。

## 进阶篇

### 这套工作区是怎么设计的

如果你不满足于“会用”，还想理解“为什么这样设计”，这部分会给你答案。

#### 设计哲学

这套工作区围绕三个核心原则展开:

**1. 人类决策，Agent 执行**

人类负责:理解题目、确定建模方向、设定约束条件、审核最终论文。
Agent 负责:读取数据、运行模型、生成代码、渲染图表、起草论文。

关键设计是 `workspace/inbox/` —— 人类把研究笔记、赛题理解、初步思路放入 inbox，Agent 启动时优先读取这些“人类决策信号”，而不是从零开始理解题目。

**2. 证据可追溯**

论文中的每一个数字都必须能追溯到具体的代码、数据和日志文件。这就是 `04-results/` + `05-evidence/` 存在的意义。`05-evidence/evidence-index.csv` 是论文主张和证据文件之间的桥梁。

评审老师不需要信任我们说的任何一句话，只需要检查证据索引中的每个条目是否真实存在。

**3. 工程与论文分离**

工程信息(运行日志、依赖版本、安装步骤、目录树)放在 `00-admin/` 和 `04-results/` 中。论文正文只保留科学上必要的内容。不把工程信息复制粘贴进论文充篇幅。

#### 为什么要独立审校？

写作和审校由同一方完成时，盲点是无法避免的。写作者天然倾向于相信自己写的东西没问题。

因此，`07-review/` 目录独立于 `06-paper/`，发布前必须运行 `cumcm-paper-audit` Skill 进行独立检查。审校报告保存在 `07-review/` 中，修复必须回到权威数据、代码或论文源文件中完成，不能直接在审校目录里改成品。

#### 为什么 Agent 要先读人类思路？

Agent 的最大风险是“自说自话”——它可能选错方向、编造文献、忽略约束条件，但看起来依然逻辑自洽。

把人类的研究笔记放入 `inbox`，强制 Agent 在启动时读取，是在给 Agent 上一道 **“前置信标”**。它告诉 Agent:

- 人类已经确认的方向是什么
- 哪些是硬性约束
- 哪些是待验证的猜想
- 哪些是绝对不能做的(比如禁止外推、禁止神经网络)

人类不一定正确，但人类的决策逻辑可以为 Agent 提供“为什么选这个模型”的解释框架，降低 Agent 选错方向的概率。

### 人机协作

#### 人类预建模与Agents协作

以下是某次比赛中，人类在 Day 1 使用 C 端 AI(网页版)完成研究后，放入 `workspace/inbox/` 的建模思路摘要。它展示了“人类决策 → Agent 执行”模式的实际产物。

```markdown
### 2021 年数模 B 题《乙醇偶合制备 C4 烯烃》建模前思路摘要

**核心策略**:重逻辑、轻算法、紧贴数据

**赛题核心解读**
- 输入(自变量):温度、Co 负载量、Co/SiO₂ 与 HAP 装料比、乙醇浓度(流速)
- 输出(因变量):乙醇转化率、C4 烯烃选择性
- 终极目标:C4 烯烃收率 = 转化率 × 选择性 最大化
- 难点:转化率和选择性往往是“跷跷板”关系，需要通过模型寻找最佳平衡点

**整体建模路线**
第 1 问(画图看趋势)→ 第 2 问(建立回归模型)→ 第 3 问(网格寻优)→ 第 4 问(局部加密)

**关键约束**
- 变量严格限制在附件数据边界内，禁止外推
- 附件 1 只有几十组数据，禁止使用神经网络或复杂集成算法
- 网格搜索步长 1℃ 已足够，341.7℃ 这类数值属于伪精度

**未验证猜想(Agent 可选择性探索)**
- 附件二的其他产物选择性能否拓展分析？
- 其他产物选择性对主要产物是否有影响？
- 时间关系能否作为创新点？

**论文呈现建议**
- 等高线图比堆叠公式更有说服力
- 结合化学常识解释“跷跷板”现象
- 结果表格化呈现，精确度保留到整数位即可
```

人类在 Day 1 完成这份笔记后，将其放入 `workspace/inbox/2025-xx-xx-cumcm-b/`。Day 2 启动 Agent 时，第一件事就是读取这份笔记，然后基于人类确定的框架开始工作。

Agent 不需要理解化学机理，它只需要:
1. 读取人类确认的约束条件(禁止外推、禁止神经网络)
2. 按照人类划定的路线生成代码
3. 对“未验证猜想”选择性地探索
4. 论文呈现时参考人类的建议

这就是“人类决策 + Agent 执行”模式的核心实践。

### 审校分两层：自动审校 + 人工审校

写作和审校由同一方完成时容易留下盲点。发布前使用 `cumcm-paper-audit` Skill：脚本核验稳定、客观的机器契约，独立 Reviewer 核对模型、证据、论证和视觉表达，二者共同写入唯一的 `07-review/final-audit.md`。人类再对题意、现实假设、决策价值和最终提交负责；自动检查、Reviewer judgment 与发布门禁的边界只以[最终审查标准](docs/standards/paper-quality-audit.md)为准。

## 最后提醒

具体项目的计算、编译和审校命令，必须记录在该项目的 `00-admin/runbook.md` 中。

**根目录不得放置项目脚本、论文、结果、临时文件或新增的专题文档**——它们各有各的位置。如果发现不知道该放哪，先查 `docs/architecture/workspace-layout.md`。
