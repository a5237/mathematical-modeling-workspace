# 建模环境指南

本文档只提供工作区级 Python 环境、依赖同步和自检命令。环境、版本、项目运行手册、参数与复现记录的要求只以 `docs/standards/data-reproducibility.md` 为准。

## Python 环境

- 本机环境目录：`.venv-modeling/`
- 锁定依赖：`config/python/requirements-modeling.txt`
- 通用环境检查：`tools/check-modeling-env.py`
- 工具运行缓存：`var/temp/`

不激活环境时统一使用工作区解释器：

```powershell
.\.venv-modeling\Scripts\python.exe <script.py>
```

## 安装或同步依赖

```powershell
.\.venv-modeling\Scripts\python.exe -m pip install -r config/python/requirements-modeling.txt
```

`config/python/requirements-modeling.txt` 是工作区依赖入口。新增依赖时先在当前环境安装和验证，再更新该文件；哪些版本和外部依赖需要进入项目复现记录，执行数据与复现规范。

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

临时脚本的运行约定：需要人/Agent 阅读的中文结果不要依赖终端显示——Windows 控制台默认代码页 936 会把 UTF-8 输出显示成乱码，一次性 `python -c` 还可能抛 `UnicodeEncodeError`。把结论写入 `var/temp/` 下的 UTF-8 文件（或使用工具的稳定输出）后再读取；也不得从截断或乱码的终端输出推断数据。

项目路径、输入输出、随机种子、预计运行时间、外部求解器和论文编译命令的权威要求执行 `docs/standards/data-reproducibility.md`；本指南不另行定义。
