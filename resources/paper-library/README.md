# 优质论文参考库

本目录集中保存数学建模优秀论文、阅读记录以及单独标识的格式排版样例。学习、记录与正式引用边界统一执行 `docs/guides/pre-writing-learning.md` 的 `PWL-GATE-001`。

---

## 目录结构

```text
resources/paper-library/
├── 00-format-layout/              # 按赛事归档的格式与排版样例
│   ├── README.md                  # 样例角色、使用边界与文件校验
│   ├── cumcm/                     # 结构学习只计同赛事样本，目录键与项目 profile 一致
│   │   ├── A165.pdf
│   │   ├── A092.pdf
│   │   ├── A127.pdf
│   │   ├── A101.pdf
│   │   └── processed/             # 由样例渲染出的页面与图形摘录
│   └── mcm-icm/                   # 英文样例：2022 MCM-B/C、2025 MCM-C、2025 ICM-E
│       ├── B22139705.pdf
│       ├── C22088345.pdf
│       ├── C2501869.pdf
│       ├── E2508861.pdf
│       └── processed/
│
├── 01_运筹与决策优化/              # 方法学类目，跨赛事可复用
│   ├── README.md            # 本类算法索引（0-1规划、遗传算法、动态规划）
│   ├── abstract/       # 论文精读摘要与算法摘录
│   └── full/           # 完整论文或全文 Markdown 资料
│
├── 02_物理机理与仿真/        # 方法学类目，跨赛事可复用
│   ├── README.md            # 本类算法索引（微分方程、物理反演、几何运动学）
│   ├── abstract/       # 论文精读摘要与算法摘录
│   └── full/           # 完整论文或全文 Markdown 资料
│
└── 03_统计推断与数据驱动/    # 方法学类目，跨赛事可复用
    ├── README.md            # 本类算法索引（混合效应、机器学习、回归预测）
    └── full/           # 完整论文或全文 Markdown 资料
```

`01`–`03` 按数学方法归类，不绑定任何赛事题号。题号到类目的映射属赛事属性，登记在当前项目赛事 profile 的工作区设定段（CUMCM 见 `config/contests/cumcm/rules.md` 第 4 节）。新增赛事时，在 `00-format-layout/` 下按该 profile 目录键新建同级子目录存放其格式样例。
