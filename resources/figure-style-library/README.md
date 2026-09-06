# 科研图片风格参考库

本目录提供一小组科研图片审美锚点，供 Agent 在已确定正确图型和视觉编码之后校准视觉语言。它不是数据源、模型证据、论文插图仓库或必须照抄的模板。

## 内容

- `manifest.csv`：参考项索引，说明每项适合学习和明确不应复制的内容；
- `references/*.png`：工作区用合成数据生成的可复现参考图；
- `references/overview.png`：合成参考图快速浏览页；
- `references/nature/*.png`：从 Nature / Nature Communications 官方媒体服务器取得的开放许可成图，仅作审美锚点；
- `references/nature/ATTRIBUTION.md`：Nature 参考图的逐图作者、题名、DOI、许可、原图链接、取得日期和完整性哈希；
- `../../tools/render-figure-style-library.py`：工作区生成样例的权威脚本。

根目录下的工作区生成样例使用固定随机种子和合成数据，只演示字体、轴线、配色、线点层级、留白、图例、注释、科学三维和多面板一致性。`references/nature/` 中的成图来自明确采用 CC BY 4.0 的开放获取论文，并保持官方媒体服务器提供的原始 PNG 不变。无论哪类参考，样例中的数值、变量、模型、注释、结构和结论都不得进入任何竞赛项目。

Nature 参考图的定位尤其严格：它们用于观察旗舰刊实际采用的字体与面板层级、克制配色、线点关系、共享图例/色标和紧凑布局，不是“Nature 模板”。Nature 官方也不鼓励在论文中直接复用或改编既有展示项；正式作图必须使用项目权威数据与模型重新生成。

## 使用

1. 先读 `docs/standards/paper-figures.md` 并完成目标图的语义与图型决策。
2. 通过 `manifest.csv` 按视觉问题选取少量参考项，不要求与目标图同型。
3. 只提取需要的样式属性，并在项目 `00-admin/figure-selection-record.md` 中记录参考标识与使用边界。
4. 从项目权威数据重新生成图片，在最终尺寸下按 `PW-FIG-001` 审查。

若选用 `style-nature-*` 项，还须查看 `references/nature/ATTRIBUTION.md`，不得将其复制到项目结果、论文正文、演示文稿或交付件中。对外再分发时保留原作者、来源和 CC BY 4.0 许可信息。

完整方法见 `docs/guides/scientific-figure-aesthetics.md`。

## 重新生成

在仓库根目录运行：

```powershell
.\.venv-modeling\Scripts\python.exe tools\render-figure-style-library.py
```

生成脚本只覆盖本目录 `references/` 中由它声明的文件，不读取任何正式项目数据。
它不会覆盖 `references/nature/` 中的外部参考图。
