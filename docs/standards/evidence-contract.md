# 数学建模证据契约

> control_id: `WG-EVID-001`
>
> 作用：统一规定论文主张、机器产物和文献台账的可追溯结构。生产、写作和审校流程只引用本契约，不另行维护字段或状态规则。

## 1. 主张与证据

每条会影响结论的主张必须具有稳定 `claim_id`，并至少指向一种可核查证据：程序输出、表格、图片、运行日志、原始数据字段、推导或已检索文献。

`05-evidence/evidence-index.csv` 必须包含：

- `claim_id`：如 `C-Q01-001`；
- `question_id`：如 `q01`；
- `claim`：准备写入论文的简洁主张；
- `evidence_type`：`table`、`figure`、`metric`、`log`、`derivation`、`literature`；
- `source_path`：相对项目根目录的实际文件；
- `generator`：生成该证据的脚本、命令或人工推导说明；
- `generated_at`：ISO 8601 时间；
- `status`：仅允许 `draft`、`verified`、`rejected`。

发布前，所有已写入论文的主张必须为 `verified`。同一具体数值只能有一个权威机器可读来源；论文表格和图应由该来源再生，禁止手工改数或把未保存的控制台输出作为唯一依据。

## 2. 文献台账

`05-evidence/literature-ledger.csv` 必须包含：

`citation_key,title,authors,year,doi_or_url,retrieved_at,used_in,verified`

`verified=yes` 仅表示已经打开原始来源，并核对题名、作者、年份以及来源对正文相邻主张的实际支持关系。搜索摘要、AI 生成书目、未打开的二手引用和算法资源库中的候选书目不得直接进入正式参考文献。

论文文献的数量、组成和正文引用方式由 `docs/standards/paper-writing.md` 规定；本契约只负责来源真实性、登记字段和证据状态。

## 3. 执行边界

- `docs/standards/workspace-governance.md` 规定证据文件的位置、生命周期和工程门禁。
- `.codex/skills/cumcm-paper-production/SKILL.md` 负责在生产过程中登记。
- `.codex/skills/cumcm-paper-audit/SKILL.md` 负责核对现有记录，不得在审校时补造证据。
