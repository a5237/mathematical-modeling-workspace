# 新需求入口

每次新需求先建立推荐的 `yyyy-mm-dd-short-name/` 子目录，保存 `request.md`、题目要求和用户原始附件。Agent 收到 inbox 任务后必须：

1. 读取要求与附件并确认比赛、年份、题号和数据类型；
2. 调用生产 Skill 初始化器在 `workspace/projects/<project-id>/` 创建推荐骨架；
3. 将题面/说明归入 `01-problem/`，原始数据归入 `02-data/raw/`，其它附件按职责分类；
4. 更新 `01-problem/problem-checklist.md`，随后触发 `WG-MODEL-001`、数据审计、证据、`PWL-GATE-001`、论文生产和 Final Audit；
5. 确认项目副本完整后清空对应入口，避免两份原始材料竞争。

inbox 名称属于 Agent 约定，不设置普通命名 hard gate；分类与项目工作流本身保持强制。
