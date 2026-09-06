# 通用工具

仅保存可跨项目复用的环境自检、格式转换和辅助程序。某一道题专用的模型代码必须放入对应项目的 `03-models/`。工具产生的临时输出统一写入 `var/tmp/`。

- `check-modeling-env.py`：检查 Python 依赖、求解器和基础计算能力。
- `check-workspace-layout.py`：检查仓库分层、根目录白名单、废弃路径和目录命名。
- `control_contracts.py`：从权威 Markdown 规范读取机器执行的字段与阈值契约，供项目初始化器和审校器导入；该文件是内部库，不提供独立命令行输出。
- `update.bat`：当`requirements-modeling.txt` 更新或发现缺包时可不重建环境直接补全缺失依赖。
- `extract-spreadsheet.py`：只读检查单个或一批 Excel 工作簿，并把指定工作表流式提取为带审计记录的 CSV/TSV；适用于十几万行以上的通用数据导入。

## Excel 大表检查与提取

工具支持现代 `.xlsx`、`.xlsm`、`.xltx`、`.xltm`，并兼容旧式 `.xls`。现代格式使用 `openpyxl` 的只读流式模式，不把整张表一次性载入 DataFrame。原始文件不会被修改；输出已存在时默认拒绝覆盖。

批量盘点多个附件或整个原始数据目录：

```powershell
.\.venv-modeling\Scripts\python.exe tools/extract-spreadsheet.py inspect-many `
  workspace/projects/cumcm-2026-a/02-data/raw `
  --recursive `
  --sample-rows 2 `
  --report var/tmp/cumcm-2026-a-workbooks.json
```

批量报告逐个记录工作簿哈希、工作表、表头、报告尺寸和样本；单个损坏文件会被记为错误，同时继续检查其它文件，并以非零状态结束。

先检查工作表、表头、规模和少量样本：

```powershell
.\.venv-modeling\Scripts\python.exe tools/extract-spreadsheet.py inspect `
  workspace/inbox/2026-01-01-example/source.xlsx
```

提取指定工作表和列：

```powershell
.\.venv-modeling\Scripts\python.exe tools/extract-spreadsheet.py extract `
  workspace/projects/cumcm-2026-a/02-data/raw/source.xlsx `
  workspace/projects/cumcm-2026-a/02-data/processed/source.csv `
  --sheet 数据 `
  --columns 编号 时间 测量值 类别
```

提取后默认同时生成 `source-audit.json`，记录输入/输出 SHA-256、工作表、字段、行数、缺失单元格、重复行、观测类型、耗时和表头修复。CSV/TSV 与审计 JSON 作为一对提交；任一提交失败时会恢复覆盖前文件。常用选项：

- `--sheet-index 2`：按从 1 开始的序号选取工作表；与 `--sheet` 互斥。
- `--header-row 3`：指定从 1 开始的表头行号。
- 表头首尾空格会统一去除并写入审计警告；`--repair-headers` 还会显式命名空表头并为重复表头添加后缀，默认遇到这两类歧义即停止。
- `--max-rows 1000`：先做小规模试提取。
- `--duplicate-check auto|memory|disk|off`：重复行精确检查策略；默认 `auto` 在内存达到阈值后切换到 `var/tmp/` 中的临时 SQLite 索引。
- `--duplicate-memory-rows 100000`：调整 `auto` 模式的切换阈值。
- `--skip-duplicate-check`：兼容旧命令的停用重复检查别名，新命令优先使用 `--duplicate-check off`。
- `--formulas`：输出公式表达式；默认输出工作簿上次保存的缓存值。
- `--overwrite`：显式允许替换既有输出和审计文件。

注意：

- `.xlsx` 的公式缓存可能过期；关键公式值应先用能重新计算公式的工作簿运行时核验。
- 存为数值且仅靠单元格格式显示前导零的编号，会按数值提取；关键标识应在源表中存为文本，或在项目专用清洗代码中明确转换。
- 本工具只做通用检查和无业务假设的提取。异常值规则、缺失值填补、特征工程等项目专属处理必须保存在对应项目的 `03-models/`，派生数据写入 `02-data/processed/`。
