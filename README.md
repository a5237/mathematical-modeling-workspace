# 全国大学生数学建模大赛工作区

这是一个用于全国大学生数学建模大赛（CUMCM）的私人工作区，用于按项目组织赛题、数据、模型、结果、论文和交付材料。

## 目录约定

- `00-inbox/`：新收到、尚未归类的需求与附件。
- `projects/`：正式项目，采用 `<contest>-<year>-<problem>` 命名。
- `templates/`：可复用模板。
- `shared-tools/`：跨项目通用工具。
- `paper-library/`：按竞赛、年份和题号整理的优秀论文参考材料。
- `archive/`：历史归档，不作为当前项目来源。
- `paper-system/`：工作区的项目结构与命名规则。
- `tmp/`：临时渲染、缓存和调试产物，仅长期保留说明文件。

## 项目内文件路由

每个正式项目使用 `projects/<contest>-<year>-<problem>/` 目录，并按以下路径归档：

- `00-admin/`：项目配置、运行说明和管理记录。
- `01-problem/`：题目与题意核对材料。
- `02-data/raw/`：原始附件，只读保存；`02-data/processed/`：清洗后的数据。
- `03-models/`：可运行的模型、参数和算法实现。
- `04-results/`：程序生成的图、表、指标和日志。
- `05-evidence/`：证据索引、文献登记和工具使用记录。
- `06-paper/`：论文源文件及其引用的图表副本。
- `07-review/`：审校记录与发布检查结果。
- `08-delivery/`：最终交付材料。

新建的脚本、图片、表格、PDF 和临时文件不应散落在根目录；应先按上述目录归档后再纳入版本控制。`tmp/` 仅用于临时产物，除说明文件外不保留长期内容。

## 快速入口

- [数模环境说明](数模环境说明.md)
- [数学建模工作区规范](数学建模工作区_Agent强制规范.md)
- [数学建模论文写作规范](数学建模论文写作_Agent强制规范.md)
- [项目命名规则](paper-system/NAMING.md)
- [论文生产流程](paper-system/README.md)
- [优质论文参考库](paper-library/README.md)

## 常用命令

```powershell
# 检查建模环境、依赖和外部工具
.\.venv-modeling\Scripts\python.exe shared-tools/check-modeling-env.py
```

具体项目的计算、编译和审校命令应记录在该项目的 `00-admin/runbook.md` 中，不在工作区 README 中绑定某一道历史赛题。
