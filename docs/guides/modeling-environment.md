# 建模环境指南

本文档只说明工作区级 Python 环境、依赖锁定和环境自检。具体项目的计算、编译、资源需求和成功标志必须写入项目 `00-admin/runbook.md`。

## Python 环境

- 本机环境目录：`.venv-modeling/`
- 锁定依赖：`config/python/requirements-modeling.txt`
- 通用环境检查：`tools/check-modeling-env.py`
- 工具运行缓存：`var/tmp/`

不激活环境时统一使用工作区解释器：

```powershell
.\.venv-modeling\Scripts\python.exe <script.py>
```

## 安装或同步依赖

```powershell
.\.venv-modeling\Scripts\python.exe -m pip install -r config/python/requirements-modeling.txt
```

依赖清单是工作区环境的可复现锁定文件，不用于保存某一道题的专属参数。新增依赖时应确认用途、在当前环境实际安装和验证，再更新锁定文件；不得把整台机器的无关软件写入清单。

## 环境自检

```powershell
.\.venv-modeling\Scripts\python.exe tools/check-modeling-env.py
```

自检会检查主要科学计算、统计、优化、可视化和 Notebook 依赖，并执行小规模冒烟测试。生成的图片和 Matplotlib 缓存写入 `var/tmp/`，可以安全清理。

Graphviz 的 Python 接口与系统可执行程序是两个独立依赖；即使 `pydot` 可导入，仍需单独确认 `dot` 是否在 `PATH` 中。PyTorch 不作为默认依赖，只有具体模型需要时才在项目运行手册中登记。

## 项目运行约定

项目入口一律使用仓库相对路径，例如：

```powershell
.\.venv-modeling\Scripts\python.exe workspace/projects/<project-id>/03-models/q00-run-all.py
```

严禁在脚本中硬编码用户名或个人绝对路径。项目的输入输出映射、随机种子、预计运行时间、外部求解器和论文编译命令均由项目自己的 `00-admin/runbook.md` 负责。
