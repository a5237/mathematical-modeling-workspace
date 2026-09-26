# 优质论文参考库

本目录集中保存数学建模优秀论文、阅读记录以及单独标识的格式排版样例。学习、记录与正式引用边界统一执行 `docs/guides/pre-writing-learning.md` 的 `PWL-GATE-001`。

---

## 目录结构

```text
resources/paper-library/
├── 00-format-layout/              # 跨题型格式与排版参考；不得作为模型或结果来源
│   ├── README.md                  # 赛事隔离、样例角色、使用边界与文件校验
│   ├── cumcm/                     # 国赛样例：A165/A092/A127/A101.pdf + processed/
│   └── mcm-icm/                   # 美赛样例：B22139705/C22088345/C2501869/E2508861.pdf + processed/
│
├── 01_运筹与决策优化/        # 对应 B 题、D 题
│   ├── README.md            # 本类算法索引（0-1规划、遗传算法、动态规划）
│   ├── abstract/       # 论文精读摘要与算法摘录
│   └── full/           # 完整论文或全文 Markdown 资料
│
├── 02_物理机理与仿真/        # 对应 A 题
│   ├── README.md            # 本类算法索引（微分方程、物理反演、几何运动学）
│   ├── abstract/       # 论文精读摘要与算法摘录
│   └── full/           # 完整论文或全文 Markdown 资料
│
└── 03_统计推断与数据驱动/    # 对应 C 题、E 题
    ├── README.md            # 本类算法索引（混合效应、机器学习、回归预测）
    └── full/           # 完整论文或全文 Markdown 资料
```

## 赛事归属

- `00-format-layout/` 承载**结构与排版**学习，按赛事分子目录：`cumcm/`、`mcm-icm/`。结构、摘要组织、篇幅分配与表达策略的学习只能取当前项目赛事的子目录。
- `01`–`03` 按数学类型组织，内容取自 CUMCM 论文，属**方法与论证逻辑**类资源，跨赛事可用，但不得计入 `PWL-GATE-001` 的结构学习范文数量；口径见 `docs/guides/pre-writing-learning.md` §2。
