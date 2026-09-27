# 虚拟环境快速入口

本文件仅作为根目录环境引导入口。安装与自检的操作步骤见 [`docs/guides/modeling-environment.md`](docs/guides/modeling-environment.md)，该文件会把你指向环境要求的权威规范。

`.venv-modeling/` 不可跨电脑复制；每台电脑应在本地重新创建。Windows 用户可在工作区根目录执行：

```powershell
.\setup.bat
```

环境建立后运行：

```powershell
.\.venv-modeling\Scripts\python.exe tools/check-modeling-env.py
```

只有输出 `RESULT: PASS` 才表示工作区级建模环境自检通过。具体项目的依赖、运行入口、资源需求和成功标志仍记录在项目自己的 `00-admin/runbook.md`。
