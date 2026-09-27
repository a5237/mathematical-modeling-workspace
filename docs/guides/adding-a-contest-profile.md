# 新增赛事 profile

接入一个赛事只新建目录与模板，不改动 Core。分层判据以 `docs/standards/workspace-governance.md` 的 `WG-LAYER-001` 为准。

## 必填项

`config/contests/<profile>/profile.yaml`：

- `contests`：本 profile 服务的赛事标识列表；标识唯一性与项目 ID 的对应关系以 `docs/standards/naming.md` 为准。
- `contract_keys`：本 profile `rules.md` 内 machine-contract 块提供的键，须与块内键完全一致。
- `paper_framework`：相对 `resources/templates/` 的论文框架路径。同一论文形状家族的多个 profile 可指向同一份框架。

`config/contests/<profile>/rules.md`：

- 第一部分 官方条款：`last_verified` 与本段的 machine-contract 块（页数与体积上限等官方值），块必须位于本段之内。
- 第二部分 本赛事下的工作区设定：章节结构与节名、标题编号样式与对齐、统计区段口径与长度线、交付集（`extra_delivery_directories`、`delivery_manifest_path`、`delivery_manifest_title`，无则不声明）、学习样本目录与题号映射、本赛事要求携带的官方标识。
- profile 目录只允许这两份文件，其余文件会被契约加载器拒绝。

## 机器口径

统计区段的定界标签、导出方式与"审校须排在编译之后"的次序约束，只以 `docs/standards/paper-quality-audit.md` 第 4 节为准；框架按该节给出的标签名放置标签即可，本指南不复述。

## 语料与验证

- `resources/paper-library/00-format-layout/<profile>/` 先建目录并放入不少于 `learning_paper_minimum` 篇同赛事结构范文，否则初始化器生成的学习记录指向不存在的路径。
- 完成后依次跑：`python -m unittest discover -s tools/tests -p "test_*.py"`、`python tools/check-workspace-layout.py`、`--contest <标识>` 的初始化冒烟与 `--phase draft` 审校。
