# 通用工具

仅保存可跨项目复用的环境自检、格式转换和辅助程序。某一道题专用的模型代码必须放入对应项目的 `03-models/`。工具产生的临时输出统一写入 `var/tmp/`。

- `check-modeling-env.py`:检查 Python 依赖、求解器和基础计算能力。
- `check-workspace-layout.py`:检查仓库分层、根目录白名单、废弃路径和目录命名。
- `control_contracts.py`:从权威 Markdown 规范读取机器执行的字段与阈值契约，供项目初始化器和审校器导入；该文件是内部库，不提供独立命令行输出。
- `update.bat`:增量补全缺失的依赖(不重建环境) ，当`requirements-modeling.txt` 更新或发现缺包时可不重建环境直接补全缺失依赖。
