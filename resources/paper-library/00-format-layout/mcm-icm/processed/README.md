# MCM/ICM 格式排版样例预处理索引

> 原 PDF 保持权威；预处理产物用于低 token 检索、按页定位和选择性视觉检查。

| 样例 | 页数 | 插图 | 表格 | 章节条目 | 入口 |
|---|---:|---:|---:|---:|---|
| `../../B22139705.pdf` | 25 | 15 | 5 | 43 | [b22139705/README.md](b22139705/README.md) |
| `../../C22088345.pdf` | 25 | 19 | 2 | 50 | [c22088345/README.md](c22088345/README.md) |
| `../../C2501869.pdf` | 25 | 12 | 11 | 40 | [c2501869/README.md](c2501869/README.md) |
| `../../E2508861.pdf` | 27 | 19 | 3 | 42 | [e2508861/README.md](e2508861/README.md) |

## 通用原则

- 默认只读取目标样例的 `outline.md`、`full-text.md` 或 `visual-index.md`。
- 不一次性加载全部页图；先用总览定位，再打开单页或单幅裁图。
- 自动提取内容不得替代原 PDF，也不得作为正式引用或项目结果证据。

## 美赛样例的提取口径

- 章节索引取自 PDF 书签（LaTeX 目录导出）；Summary Sheet、Contents 和 `Report on Use of AI` 等书签未覆盖的结构性页面由文字层关键词补齐。
- 插图与表格由英文题注定位：`Figure N:`、`Figure N 标题`、`Table N:` 均可识别，段落行首的正文引用（如 `Figure 18 compares …`）按"独立成行或有分隔符"规则排除。
- `E2508861.pdf` 由 Word 转 PDF，公式字符在文本层成对重复，且题注常与正文同块，裁图可能带入相邻正文；该篇的公式与变量名以原页图为准。
- 页数口径：`E2508861.pdf` 的 27 页 = 25 页方案 + 2 页不计页的 `Report on Use of AI`，与 `config/contests/mcm-icm/rules.md` 的 `body_page_maximum` 口径一致。
