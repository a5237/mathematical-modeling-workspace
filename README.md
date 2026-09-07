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
3. Agent 会整理材料、建立项目，并开始分析、计算和写作
4. 人类持续确认建模方向，并在初稿完成后负责人工校审和最终交付

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
├── AGENTS.md               # Agent 入口与强制路由
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
| `tools/extract-spreadsheet.py` | 批量检查 Excel 附件并流式提取带审计的 CSV/TSV | 附件较多或工作表较大时 |
| `AGENTS.md` | Agent 的行为规则和强制门禁 | 如果你用 Codex/Claude Code 等 AI 工具 |
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
| 文件怎么放、目录怎么用 | [工作区治理规范](docs/standards/workspace-governance.md) |
| 证据怎么追溯 | [证据契约](docs/standards/evidence-contract.md) |
| 论文怎么写、怎么排版 | [论文写作规范](docs/standards/paper-writing.md) |
| 论文配图怎么做 | [论文图片与科研可视化规范](docs/standards/paper-figures.md) |
| 论文怎么审、何时复查 | [最终审查与竞争力评分标准](docs/standards/paper-quality-audit.md) |
| 怎么命名文件和项目 | [命名规范](docs/standards/naming.md) |
| 环境怎么配 | [建模环境指南](docs/guides/modeling-environment.md) |
| 论文生产流程是什么 | [论文生产流程](docs/guides/paper-production.md) |
| 写作前要做什么 | [写作前强制学习流程](docs/guides/pre-writing-learning.md) |
| 有什么算法可以参考 | [算法资源库索引](resources/algorithm-library/index.md) |
| 有什么模板可以用 | [资源区](resources/README.md) |
| 项目区在哪 | [项目区](workspace/projects/README.md) |

## 接下来做什么？

### 一次比赛的基本流程

1. 跑完 `setup.bat`，确认环境正常
2. 把新赛题的材料放入 `workspace/inbox/`
3. 把你对题目的理解、倾向采用的方法和明确限制一起告诉 Agent
4. 在关键建模选择处及时确认方向，不要等论文写完才发现问题
5. 初稿完成后进行人工校审，再整理最终提交文件

### 人工校审（人类完成）

Agent 可以检查文件、计算结果和常见格式问题，但论文是否可信、清楚、有说服力，最后仍要由人来判断。建议把校审分成三遍。

第一遍只读摘要、各问的最终答案和结论。看一个不了解项目的人能否迅速明白：题目要解决什么、用了什么办法、得到了什么结果，以及这些结果有什么意义。若答案藏在长篇推导里，先改表达顺序。

第二遍顺着论证往下读。重点判断假设是否合理，模型是否真的回答了题目，关键结论能否从数据、公式和实验中得到，图表是否帮助理解而不是只起装饰作用。对任何“看起来很正确”的数字，都回到原始结果核对一次。

第三遍只看最终 PDF 和提交包。像普通读者一样逐页翻阅，检查有没有难读、跳页、遮挡、模糊或前后矛盾的地方；再确认文件齐全、可以打开、没有身份信息，也没有把临时文件带进提交包。

发现问题时，应回到数据、代码、图表或论文源文件修改，再重新生成成品；不要直接在最终 PDF 上临时遮改。需要逐项核对格式和交付要求时，再查看[论文写作规范](docs/standards/paper-writing.md)和[最终审查标准](docs/standards/paper-quality-audit.md)。

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

写作者熟悉自己的思路，往往会自动补上文中没有说清楚的部分。换一个没有参与写作的人重新阅读，更容易发现跳步、含糊结论和图文不一致。

机器检查适合发现缺文件、数字冲突和明显格式问题，但机器通过不等于论文已经写好。独立校审和最后的人工通读，关注的是整篇论文能不能让评审相信、看懂并记住。

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

## 最后提醒

新题目先放进 `workspace/inbox/`，正式工作放在对应项目里，临时文件放进 `var/tmp/`。如果不知道文件该放哪，查看[工作区架构](docs/architecture/workspace-layout.md)。
