# MCM/ICM 现行官方规则基线

> control_id: `OFFICIAL-MCM-ICM-001`
>
> last_verified: `2026-09-26`
>
> 作用：集中保存会随年度变化的 COMAP（美国大学生数学建模/交叉学科建模竞赛，MCM/ICM）规则快照，当前对准 2027 届（2027-01-28 至 2027-02-01）。正式参赛或提交前必须重新打开官方来源核对；当届新规和用户当前明确要求优先于本文件。

```toml machine-contract
paper_maximum_bytes = 25000000
body_page_maximum = 25
```

上方 `paper_maximum_bytes` 供机器执行提交附件大小上限（官方措辞为“小于 25 MB”，按十进制取 25,000,000 字节从严执行）；`body_page_maximum` 的统计口径为**整个提交 PDF 的总页数**，含 Summary Sheet、目录、正文、参考文献、注释页、附录与代码，仅不含 25 页方案之后的 “Report on Use of AI” 一节。正式提交前仍须重核官网并同步更新本文件。

## 1. 2027 届论文与提交规则

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

## 2. AI 工具使用规则

- AI 只作辅助；解题本身不要求使用 AI，负责任的使用被允许，但模型选择与构建、代码生成、数据与结果解读、科学结论等环节依赖 AI 有风险，官方建议谨慎。
- 使用 AI 的队必须在论文中**明确标注**用了哪个模型、用于什么目的：正文用行内引用，并在参考文献列表列出全部 AI 工具。
- 在 25 页方案之后附加 “Report on Use of AI” 一节；该节无页数限制且不计入 25 页。
- 必须核实 AI 生成内容及引用的准确性、有效性与恰当性并纠正错误；须警惕 AI 复现他人文本导致的抄袭（抄袭与隐瞒 AI 使用可被取消资格或降级）。

官方来源：

- [Use of AI Tools in COMAP Contests（含示例的官方政策 PDF）](https://www.contest.comap.com/undergraduate/contests/mcm/flyer/Contest_AI_Policy.pdf)

## 3. 使用规则

1. 论文内容、通用排版与图片要求分别由 `docs/standards/paper-writing.md`、`docs/standards/paper-formatting.md`、`docs/standards/paper-figures.md` 在本官方基线上增补，不得冒充官方统一要求。
2. 工程生命周期、AI 台账和交付路由由 `docs/standards/workspace-governance.md` 管理；交付件匿名性由论文写作规范管理，其覆盖范围可以严于上述官方快照。
3. 生产和审校 Skill 只引用本文件，不维护第二套年度规则摘要。
4. 每次正式提交前更新 `last_verified`，并记录新旧规则的生效日期；不得只改年份而不重新打开来源。
5. 页数门禁执行本文件的 `body_page_maximum`（全提交口径，仅不含 AI 使用报告一节）；本赛事不设官方页数下限，工作区亦不额外设下限。
