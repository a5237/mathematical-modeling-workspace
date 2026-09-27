# MCM/ICM 官方规则与本赛事工作区约定

> control_id: `OFFICIAL-MCM-ICM-001`
>
> last_verified: `2026-09-26`
>
> 作用：集中保存 COMAP（美国大学生数学建模/交叉学科建模竞赛，MCM/ICM）的当届官方规则快照，以及本工作区为该赛事设定的门禁与论文形状，当前对准 2027 届（2027-01-28 至 2027-02-01）。正式参赛或提交前必须重新打开官方来源核对；当届新规和用户当前明确要求优先于本文件。

本文件分两部分：第一部分是**官方条款**，`last_verified` 与提交前重核只覆盖第一部分；第二部分是**本赛事下的工作区设定**，属工作区自设要求，不冒充官方规定。

```toml machine-contract
paper_maximum_bytes = 25000000
body_page_maximum = 25
```

上方 `paper_maximum_bytes` 供机器执行提交附件大小上限（官方措辞为“小于 25 MB”，按十进制取 25,000,000 字节从严执行）；`body_page_maximum` 的统计口径为**整个提交 PDF 的总页数**，含 Summary Sheet、目录、正文、参考文献、注释页、附录与代码，仅不含 25 页方案之后的 “Report on Use of AI” 一节。正式提交前仍须重核官网并同步更新本文件。

## 第一部分 官方条款

### 1. 2027 届论文与提交规则

- 提交为单个 Adobe PDF 文件，用英文录入，正文字号不小于 12 pt。
- **全提交不超过 25 页**：Summary Sheet、目录、正文、参考文献、注释页、附录、代码及题目附加要求全部计入；“Report on Use of AI” 一节不计页数且无页数限制。
- 每页页眉须含队控制号（Control Number）与页码，官方示例格式为 `Team # 0000000, Page 6 of 25`。
- 第 1 页必须是 Summary Sheet，随后依次为正文、参考文献与附录；目录计入页数。
- PDF 文件名使用队控制号，如 `0000000.pdf`；附件须小于 25 MB。
- 只提交这一个 PDF；不得附带程序、数据或其它文件，评奖不使用它们。
- 学生、指导教师和学校姓名不得出现在论文任何一页；除队控制号外不得含任何身份信息。
- 竞赛期间不得向队外任何人寻求答案、思路或信息，不得在任何媒介公开题目或解答的任何部分。
- 所有外部信息来源（网页、书籍、数据库等）必须用脚注、尾注或行内标注记录，并在参考文献列表中完整引用。

官方来源：

- [MCM/ICM Contest Rules, Registration and Instructions（2027 届）](https://www.contest.comap.com/undergraduate/contests/mcm/instructions.php)
- [官方 Summary Sheet（LaTeX 版）](https://www.contest.comap.com/undergraduate/contests/mcm/flyer/MCM-ICM_Summary.tex)

### 2. AI 工具使用规则

- AI 只作辅助；解题本身不要求使用 AI，负责任的使用被允许，但模型选择与构建、代码生成、数据与结果解读、科学结论等环节依赖 AI 有风险，官方建议谨慎。
- 使用 AI 的队必须在论文中**明确标注**用了哪个模型、用于什么目的：正文用行内引用，并在参考文献列表列出全部 AI 工具。
- 在 25 页方案之后附加 “Report on Use of AI” 一节；该节无页数限制且不计入 25 页。
- 必须核实 AI 生成内容及引用的准确性、有效性与恰当性并纠正错误；须警惕 AI 复现他人文本导致的抄袭（抄袭与隐瞒 AI 使用可被取消资格或降级）。

官方来源：

- [Use of AI Tools in COMAP Contests（含示例的官方政策 PDF）](https://www.contest.comap.com/undergraduate/contests/mcm/flyer/Contest_AI_Policy.pdf)

## 第二部分 本赛事下的工作区设定

本部分是工作区为该赛事设定的门禁、结构与交付集，不冒充官方统一要求，因此**不新增机器契约键**：本赛事不设页数与字数下限（`body_page_minimum`、`body_word_minimum` 缺省即不限），编号图与编号表下限由 Core 的 `body_figure_minimum`、`body_table_minimum` 统一规定。

### 3. 论文结构

COMAP 官方只规定第 1 页必须是 Summary Sheet、其后依次为正文、参考文献与附录（见第一部分），未规定正文内部的节名。下列英文骨架由本工作区为该赛事固定；`docs/standards/paper-writing.md` 第 3 节规定每个区块承担的职责，本节规定它在 MCM/ICM 论文中的节名、层级与编号。

```markdown
# Title
## Summary Sheet（Team 与 Problem 标识、总体概述、逐问任务—模型—关键结果—检验、总体结论、Keywords）

——分页与页眉执行本文件第一部分官方条款与下文页眉口径——

## Contents（目录，可选；如设置则计入 25 页）

## 1. Introduction
### 1.1 Background
### 1.2 Restatement of the Problem
## 2. Analysis of the Problem
### 2.1 Analysis of Question 1 …（按题目实际任务数增减）
## 3. Assumptions and Justifications
## 4. Notation
## 5. Model Formulation and Solution
### 5.1 Model and Solution for Question 1
#### 5.1.1 Preliminaries（可选，见下条）
#### 5.1.2 Model Formulation
#### 5.1.3 Solution
#### 5.1.4 Results and Analysis
## 6. Model Evaluation and Generalization
### 6.1 Sensitivity Analysis
### 6.2 Strengths
### 6.3 Weaknesses
### 6.4 Model Improvement and Generalization
## 7. Conclusion
## References
## Code（可选，按问分节；官方不单独收附件，收录即计入 25 页）

（Report on Use of AI 一节的位置与不计页属性执行本文件第一部分；Notes 等补充节按需增设，计入页数）
```

- 一级标题使用阿拉伯数字 `1.`，二级 `1.1`，三级 `1.1.1`；全部左对齐，不加中文数字编号，不居中。
- 预备条件职责在本赛事由 `5.x.1 Preliminaries` 承担；该小节内容较少时可删除，把预备量并入 `Model Formulation` 开头，Core 只要求该职责被就近交代。
- Summary Sheet 的 `Keywords` 设 4—6 个，用分号分隔，不使用 `mathematical modeling`、`MATLAB` 等过宽词；这是本赛事的页面组织设定，官方未逐条规定。
- 目录可选；官方把目录页计入 25 页，设置目录前必须确认全篇页数有余量。
- 页眉左右分置：左上为 `Team # <队控制号>`，右上为 `Page <当前页> of <总页数>`，页眉下方画 0.4 pt 横线；含 Summary Sheet 在内的每一页都带页眉。
- `<总页数>` 取最后一个计入 25 页口径的页面，不含 “Report on Use of AI”；该节自身页码继续递增，页眉仍显示该总页数。
- “Report on Use of AI” 排在附录之后，不参与附录编号序列。
- `resources/templates/contests/mcm-icm/paper-framework.tex` 是本结构的 LaTeX 实现，不另行定义规则。

### 4. 统计区段与长度线

- 页数门禁执行第一部分官方条款：整个提交 PDF 不超过 25 页，`Report on Use of AI` 不计页。本赛事不设官方页数下限，工作区亦不加设下限。
- 叙述性字数：本赛事不设下限；`PW-LEN-001` 的字数门禁在该 profile 缺省即视为不限，但摘要与逐问结论仍须按 Core 给出可核验数值。
- 编号图与编号表的统计区段与页数口径一致：从 Summary Sheet 起至附录末页，`Report on Use of AI` 一节不计入。

### 5. 交付集

- 交付物只有 `08-delivery/` 下的单个英文 PDF；本赛事无支撑材料压缩包、无交付清单文件，`extra_delivery_directories` 与 `delivery_manifest_path` 均不声明。
- 可运行源程序、自主查阅数据和中间结果不单独提交；只有作为论文内容写进正文或附录的部分才受 25 页口径约束。
- 文件名使用队控制号（官方条款），PDF 元数据与图片属性按 Core 匿名性要求清洁。

### 6. 学习样本与题型映射

- 结构学习样本取 `resources/paper-library/00-format-layout/mcm-icm/`；方法与论证学习可取 `01`—`03` 三个方法类目。
- 题号映射：A 题→`02`，B 题与 D 题→`01`，C 题与 E 题→`03`；F 题与 ICM 的 G/H/I 题无固定映射，按实际使用方法就近选择并登记在项目 `00-admin/`。

## 7. 使用规则

1. 第一部分是当届官方快照；第二部分是工作区为该赛事设定的门禁、结构与交付集，不冒充官方统一要求。
2. Core 文档只引用本文件的中性锚点，不复述本文件的数值、节名与交付集。
3. 生产和审校 Skill 只引用本文件，不维护第二套年度规则摘要。
4. 每次正式提交前更新第一部分的 `last_verified`，并记录新旧规则的生效日期；不得只改年份而不重新打开来源。第二部分的变化按工作区门禁调整处理，不占用官方重核动作。
5. 页数门禁执行第一部分的 `body_page_maximum`（全提交口径，仅不含 AI 使用报告一节）；图、表与字数的统计区段见第二部分第 4 节。
