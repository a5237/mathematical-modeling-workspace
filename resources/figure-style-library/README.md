# 科研图片风格参考库

本目录提供一小组科研图片审美锚点，供 Agent 在已确定正确图型和视觉编码之后校准视觉语言。它不是数据源、模型证据、论文插图仓库或必须照抄的模板。

## 内容

- `manifest.csv`：参考项索引，说明每项适合学习和明确不应复制的内容；
- `references/*.png`：合成数据生成的参考图；
- `references/overview.png`：快速浏览页；
- `tools/render-figure-style-library.py`：权威生成脚本。

全部样例使用固定随机种子和合成数据，只演示字体、轴线、配色、线点层级、留白、图例、注释、科学三维和多面板一致性。样例中的数值、变量和结论不得进入任何竞赛项目。

## 使用

1. 先读 `docs/standards/paper-figures.md` 并完成目标图的语义与图型决策。
2. 通过 `manifest.csv` 按视觉问题选取少量参考项，不要求与目标图同型。
3. 只提取需要的样式属性，并在项目 `00-admin/figure-selection-record.md` 中记录参考标识与使用边界。
4. 从项目权威数据重新生成图片，在最终尺寸下按 `PW-FIG-001` 审查。

完整方法见 `docs/guides/scientific-figure-aesthetics.md`。

## 重新生成

在仓库根目录运行：

```powershell
.\.venv-modeling\Scripts\python.exe tools\render-figure-style-library.py
```

生成脚本只覆盖本目录 `references/` 中由它声明的文件，不读取任何正式项目数据。
