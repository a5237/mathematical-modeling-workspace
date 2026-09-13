# 通用工具

仅保存可跨项目复用的环境自检、格式转换和辅助程序。某一道题专用的模型代码必须放入对应项目的 `03-models/`。工具产生的临时输出统一写入 `var/temp/`。

- `check-modeling-env.py`：检查 Python 依赖、求解器和基础计算能力。
- `check-workspace-layout.py`：只检查根目录的高风险缓存/生成污染、批量项目产物和冲突性废弃结构；不维护根目录白名单、完整目录树或普通命名门禁。
- `control_contracts.py`：只读取权威文档中显式的 `toml machine-contract` 客观参数，供项目初始化器和静态 preflight 导入；不解析中文句式、报告模板或 Reviewer judgment。
- `update.bat`：当`requirements-modeling.txt` 更新或发现缺包时可不重建环境直接补全缺失依赖。
- `extract-spreadsheet.py`：把 `.xlsx/.xls` 快速清洗为逐工作表 CSV，也保留只读盘点和超大表流式提取模式。
- `extract-pdf-pages.py`：从 PDF 快速提取整页或归一化坐标裁剪区域，输出 PDF、PNG 或两者；默认写入 `var/temp/pdf-extracts/`。

## Excel 快速清洗与大表提取

工具支持现代 `.xlsx`、`.xlsm`、`.xltx`、`.xltm`，并兼容旧式 `.xls`。现代格式使用 `openpyxl` 的只读流式模式，不把整张表一次性载入 DataFrame。原始文件不会被修改；输出已存在时默认拒绝覆盖。

日常附件优先使用 `clean`。它默认处理全部非空工作表，删除全空行和全空列，自动采用每张表第一行非空行为表头，将字段名规范为稳定的下划线形式，把 Excel 日期/时间转换为 ISO 8601，并保守转换不会破坏前导零标识的数值文本。每张表输出一个 UTF-8 CSV，另生成不含文件哈希的轻量清洗报告：

```powershell
.\.venv-modeling\Scripts\python.exe tools/extract-spreadsheet.py clean `
  workspace/inbox/2026-01-01-example/source.xlsx
```

若输入位于正式项目的 `02-data/raw/`，默认输出到同项目 `02-data/processed/`；其它位置的工作簿默认输出到当前目录的 `02-processed/`。可用 `--output-dir` 显式覆盖。常用选项：

- `--sheet 数据` 或 `--sheet-index 2`：只清洗一张工作表；默认逐表输出。
- `--header-row 3`：覆盖自动表头识别。
- `--no-infer-types`：禁止将安全的数值文本转换为数值；带前导零的标识默认始终保留为文本。
- `--keep-empty-rows`：保留全空数据行；默认删除。
- `--overwrite`：显式允许替换已有 CSV 和清洗报告。

对于超大工作表、精确选列或 TSV 输出，继续使用 `inspect`、`inspect-many` 和 `extract`。

批量盘点多个附件或整个原始数据目录：

```powershell
.\.venv-modeling\Scripts\python.exe tools/extract-spreadsheet.py inspect-many `
  workspace/projects/cumcm-2026-a/02-data/raw `
  --recursive `
  --sample-rows 2 `
  --report var/temp/cumcm-2026-a-workbooks.json
```

批量报告逐个记录工作簿文件名、存在状态、工作表、表头、报告尺寸和样本；单个损坏文件会被记为错误，同时继续检查其它文件，并以非零状态结束。中间报告不记录或绑定文件哈希。

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

提取后默认同时生成 `source-audit.json`，记录输入/输出文件名与存在状态、工作表、字段、行数、缺失单元格、重复行、观测类型、耗时和表头修复，不记录文件哈希。CSV/TSV 与审计 JSON 作为一对提交；任一提交失败时会恢复覆盖前文件。常用选项：

- `--sheet-index 2`：按从 1 开始的序号选取工作表；与 `--sheet` 互斥。
- `--header-row 3`：指定从 1 开始的表头行号。
- 表头首尾空格会统一去除并写入审计警告；`--repair-headers` 还会显式命名空表头并为重复表头添加后缀，默认遇到这两类歧义即停止。
- `--max-rows 1000`：先做小规模试提取。
- `--duplicate-check auto|memory|disk|off`：重复行精确检查策略；默认 `auto` 在内存达到阈值后切换到 `var/temp/` 中的临时 SQLite 索引。
- `--duplicate-memory-rows 100000`：调整 `auto` 模式的切换阈值。
- `--skip-duplicate-check`：兼容旧命令的停用重复检查别名，新命令优先使用 `--duplicate-check off`。
- `--formulas`：输出公式表达式；默认输出工作簿上次保存的缓存值。
- `--overwrite`：显式允许替换既有输出和审计文件。

注意：

- `.xlsx` 的公式缓存可能过期；关键公式值应先用能重新计算公式的工作簿运行时核验。
- 存为数值且仅靠单元格格式显示前导零的编号，会按数值提取；关键标识应在源表中存为文本，或在项目专用清洗代码中明确转换。
- 本工具只做通用检查和无业务假设的提取。异常值规则、缺失值填补、特征工程等项目专属处理必须保存在对应项目的 `03-models/`，派生数据写入 `02-data/processed/`。

## PDF 页面快速截取

提取指定页并同时生成轻量 PDF 与 PNG：

```powershell
.\.venv-modeling\Scripts\python.exe tools/extract-pdf-pages.py `
  workspace/inbox/2026-01-01-example/problem.pdf `
  --pages 2,5-6 `
  --format both
```

按页面左上角为原点、使用 `0..1` 归一化坐标裁剪局部区域，适合表格、公式和附件说明：

```powershell
.\.venv-modeling\Scripts\python.exe tools/extract-pdf-pages.py `
  workspace/inbox/2026-01-01-example/problem.pdf `
  --pages 3 `
  --crop 0.08 0.25 0.92 0.72 `
  --format png
```

默认目录为 `var/temp/pdf-extracts/<pdf-name>/`，其中内容都是可删除过程材料，不进入正式交付目录。`--output-dir` 可改临时位置，`--dpi` 控制 PNG 清晰度，`--overwrite` 才允许覆盖同名截取结果。
