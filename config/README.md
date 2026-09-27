# 工作区配置

本目录只保存跨项目、可版本控制的静态配置。

- `python/requirements-modeling.txt`：建模环境的精确 Python 依赖锁定。
- `contests/<profile>/`：赛事 profile，每个目录一份 `profile.yaml`（赛事标识、契约键、论文框架指向）与一份 `rules.md`（官方条款段＋本赛事工作区设定段）。新增赛事在此处新建目录，不改动 Core；分层判据见 `docs/standards/workspace-governance.md` 的 `WG-LAYER-001`。

某一道题的模型参数和求解配置必须放在该项目的 `03-models/`，不得进入这里。
