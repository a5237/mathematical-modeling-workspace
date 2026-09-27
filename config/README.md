# 工作区配置

本目录只保存跨项目、可版本控制的静态配置。

- `python/requirements-modeling.txt`：建模环境的精确 Python 依赖锁定。
- `contests/<profile>/`：赛事 profile，每个目录固定 `profile.yaml` 与 `rules.md` 两份文件。接入新赛事的步骤见 `docs/guides/adding-a-contest-profile.md`。

某一道题的模型参数和求解配置必须放在该项目的 `03-models/`，不得进入这里。
