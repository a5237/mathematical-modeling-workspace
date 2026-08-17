# 通用工具

仅保存可跨项目复用的环境自检、格式转换和辅助程序。某一道题专用的模型代码必须放入对应项目的 `03-models/`。工具产生的临时输出统一写入 `var/tmp/`。

- `check-modeling-env.py`：检查 Python 依赖、求解器和基础计算能力。
- `check-workspace-layout.py`：检查仓库分层、根目录白名单、废弃路径和目录命名。
