# 格式排版样例预处理索引

> 原 PDF 保持权威；预处理产物用于低 token 检索、按页定位和选择性视觉检查。

| 样例 | 页数 | 插图 | 表格 | 入口 |
|---|---:|---:|---:|---|
| `A101.pdf` | 62 | 30 | 8 | [a101/README.md](a101/README.md) |
| `A092.pdf` | 53 | 33 | 8 | [a092/README.md](a092/README.md) |
| `A127.pdf` | 58 | 22 | 23 | [a127/README.md](a127/README.md) |
| `A165.pdf` | 45 | 10 | 12 | [a165/README.md](a165/README.md) |

## 通用原则

- 默认只读取目标样例的 `outline.md`、`full-text.md` 或 `visual-index.md`。
- 不一次性加载全部页图；先用总览定位，再打开单页或单幅裁图。
- 自动提取内容不得替代原 PDF，也不得作为正式引用或项目结果证据。
