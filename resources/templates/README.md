# 通用模板

保存未填写的论文、报告、清单和表格模板。

- `cumcm-paper-framework.tex`：正式论文的统一写作框架；初始化时复制为项目 `06-paper/main.tex`，后续只修改项目副本。
- `figure-selection-record.md`：轻量图片 registry；初始化时复制为项目 `00-admin/figure-selection-record.md`，普通图片只登记来源、生成器、图型和最终 PDF 结论，只有潜在误导性视觉处理才展开说明。
- `artifact-map.yaml`：项目产物快速导航模板；初始化时写入 `00-admin/artifact-map.yaml`，只按公共依赖与子问题登记下游会复用的稳定关键路径和证据 ID。通用影响链只保存一次，`depends_on_questions` 仅登记实际跨问依赖，不维护动态失效状态。

不得回写覆盖通用模板，也不得从模板另建相互竞争的平行论文或记录。

初始化阶段不创建 `07-review/final-audit.md`；该报告只在形成 Release Candidate 待审快照并完成真实审查后生成。Draft 与中间阶段只记录关键文件名、存在状态和完成状态，不维护文件哈希或持续有效的发布结论。
