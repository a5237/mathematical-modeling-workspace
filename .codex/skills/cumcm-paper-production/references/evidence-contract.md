# 论文证据契约

每条会影响结论的主张必须具有稳定 `claim_id`，并至少指向一种可核查证据：程序输出、表格、图片、运行日志、原始数据字段、推导或已检索文献。

`evidence-index.csv` 必须包含：

- `claim_id`：如 `C-Q01-001`；
- `question_id`：如 `q01`；
- `claim`：准备写入论文的简洁主张；
- `evidence_type`：`table`、`figure`、`metric`、`log`、`derivation`、`literature`；
- `source_path`：相对项目根目录的实际文件；
- `generator`：生成该证据的脚本、命令或人工推导说明；
- `generated_at`：ISO 8601 时间；
- `status`：仅允许 `draft`、`verified`、`rejected`。

发布前所有已写入论文的主张必须为 `verified`。同一具体数值只能有一个权威机器可读来源；论文表格和图应由该来源再生，禁止手工改数。

文献台账必须记录 `citation_key,title,authors,year,doi_or_url,retrieved_at,used_in,verified`。`verified=yes` 只表示已打开原始来源并核对题名、作者、年份和与正文主张的支持关系。
