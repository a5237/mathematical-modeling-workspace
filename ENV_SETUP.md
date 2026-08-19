# 虚拟环境搭建指南

本工作区使用 `.venv-modeling` 作为 Python 虚拟环境目录。

## 重要：环境不可移植

`.venv-modeling` 目录 **不可跨电脑复制使用**。原因：
- `pyvenv.cfg` 记录的是创建时 Python 解释器的 **绝对路径**。
- `Scripts\python.exe` 等可执行文件内部包含 **硬编码路径**。
- `Lib\site-packages\` 下的 `.pyd` 文件与 **操作系统、Python 版本、CPU 架构** 绑定。

因此，**每台电脑必须在本地重新创建虚拟环境**，不得复用其他电脑的 `.venv-modeling` 目录。

## Agent 行为指引

如果你是一个 AI Agent，在开始任何建模或论文任务前，请执行以下操作：

1. 检查根目录是否存在 `.venv-modeling\Scripts\python.exe`。
2. 如果不存在，或用户报告环境问题，引导用户运行 `.\setup.bat`。
3. 确认环境检查脚本 `tools\check-modeling-env.py` 输出 `RESULT: PASS` 后再继续。

## 快速重建（人类操作）

在项目根目录打开 PowerShell，执行：

```powershell
.\setup.bat