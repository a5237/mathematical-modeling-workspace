# 建模环境指南

本文档只提供工作区级 Python 环境、依赖同步和自检命令。环境、版本、项目运行手册、参数与复现记录的要求只以 `docs/standards/data-reproducibility.md` 为准。

## Python 环境

- 本机环境目录：`.venv-modeling/`
- 锁定依赖：`config/python/requirements-modeling.txt`
- 通用环境检查：`tools/check-modeling-env.py`
- 工具运行缓存：`var/temp/`
- 受支持解释器：Python 3.12、3.13、3.14

不激活环境时统一使用工作区解释器：

```powershell
.\.venv-modeling\Scripts\python.exe <script.py>
```

## 安装或同步依赖

```powershell
.\.venv-modeling\Scripts\python.exe -m pip install -r config/python/requirements-modeling.txt
```

`config/python/requirements-modeling.txt` 是工作区依赖入口。新增依赖时先在当前环境安装和验证，再更新该文件；哪些版本和外部依赖需要进入项目复现记录，执行数据与复现规范。

依赖文件变更后，除自检外必须运行全部工具测试；测试会以子进程真实调用工具与 Skill 脚本，能发现锁未覆盖的 import 与运行期回归：

```powershell
Get-ChildItem tools/tests/test_*.py | ForEach-Object { .\.venv-modeling\Scripts\python.exe $_.FullName }
```

## 环境自检

```powershell
.\.venv-modeling\Scripts\python.exe tools/check-modeling-env.py
```

自检会检查主要科学计算、统计、优化、可视化和 Notebook 依赖，并执行小规模冒烟测试。生成的图片和 Matplotlib 缓存写入 `var/temp/`，可以安全清理。

Graphviz 的 Python 接口与系统可执行程序是两个独立依赖；即使 `pydot` 可导入，仍需单独确认 `dot` 是否在 `PATH` 中。PyTorch 不作为默认依赖，只有具体模型需要时才在项目运行手册中登记。

## 项目运行约定

项目入口推荐使用仓库相对路径，例如：

```powershell
.\.venv-modeling\Scripts\python.exe workspace/projects/<project-id>/03-models/q00-run-all.py
```

需要人或 Agent 阅读的结果不要依赖终端显示，写入 `var/temp/` 下的 UTF-8 文件后再读取；不得从截断的终端输出推断数据。

项目路径、输入输出、随机种子、预计运行时间、外部求解器和论文编译命令的权威要求执行 `docs/standards/data-reproducibility.md`；本指南不另行定义。
