# 工作区 Markdown 冗余重构记录

- 执行日期：2026-09-07
- 目标：消除规范、Skill、资源入口和模板中的重复定义，保持“一处权威、其余按需引用”。
- 根目录 `README.md` 不作为 Agent 规范去冗余；根据后续要求，仅重写其中的人工校审说明，使其保持面向人的自然表达。

## 执行原则

1. 无独立职责的重复正文、清单、目录或 Skill 参考文件直接删除。
2. 仍承担导航职责的位置只保留最短必要引用，不复述阈值、字段全集或操作流程。
3. 仍被程序实际执行的校验代码保留；不通过新增“同步副本”“已废弃”“当前不用”等注释掩盖重复。
4. 精简不得删除或放宽 `WG-DATA-001`、`WG-MODEL-001`、`WG-EVID-001`、`PWL-GATE-001`、`PW-VAL-001`、`PW-FIG-001`、`OFFICIAL-CUMCM-001` 和 `PQA-RELEASE-001`。

## 已完成

| 项目 | 处理结果 |
|---|---|
| 跨文件复述 5000 字门禁 | `paper-quality-audit.md` 删除数值，只引用 `PW-LEN-001`；数值仍只在 `paper-writing.md` 定义。 |
| 匿名性对象清单 | `paper-writing.md` 第 15.3 节保留交付件全集；图片规范、质量审查、官方快照和审校 Skill 改为引用；工作区治理只保留日志、Notebook 与缓存卫生。 |
| 工程信息是否进入正文 | 保留 `workspace-governance.md` 第 0 节权威边界，删除其第 8 节和 `paper-writing.md` 原第 9.3 节的重复清单。 |
| 数据审计清单 | 完整字段只留在 `workspace-governance.md` 第 4.2 节；论文规范只说明哪些审计结论需要进入正文。 |
| Agent 阅读顺序 | 删除治理规范中的重复顺序；Agent 入口继续由 `AGENTS.md` 管理。 |
| 复杂度说明 | 工程记录规则保留在治理规范第 6.4 节，论文规范改为引用并删除同义句。 |
| 范文使用边界 | 保留 `PWL-GATE-001` 权威定义；论文规范、治理规范和算法库入口不再复述，论文参考库只保留控制编号引用。 |
| 参考图流程 | 完整方法只留在 `scientific-figure-aesthetics.md`；图片规范和参考库入口只保留职责引用。 |
| 跨载体数值与舍入一致性 | 完整检查只留在 `paper-writing.md` 第 16 节；其它位置删除或引用该节。 |
| 附录分页 | 只在 `paper-writing.md` 第 15.2 节保留，删除前文重复要求。 |
| 审校分级 | 删除重复的 `references/audit-rubric.md`，审校 Skill 直接执行 `paper-quality-audit.md` 第 7 节。 |
| 算法库目录 | `resources/algorithm-library/README.md` 删除重复算法清单、快速索引和通用建议，只保留 `index.md` 入口。 |
| 可选图片记录 | 未使用高风险视觉处理或参考图时删除对应节/字段，不保留破折号占位。 |

## 有意保留

- `audit_cumcm_project.py` 的 `FINAL_AUDIT_FIELDS` 仍用于实际校验最终报告字段，不属于死代码。本轮不增加同步注释。
- 权威文件中的 `toml machine-contract` 与同文件自然语言解释分别服务机器和人类，可同时保留。
- `AGENTS.md` 的触发式导航、各权威文件的发布检查表以及根目录 `README.md` 的人类说明具有独立用途，不按机械文本相似度删除。

## 验证

实测结果：

```text
python -m unittest tools.tests.test_audit_refactor -v  → Ran 6 tests, OK
tools/check-workspace-layout.py                        → RESULT: PASS
skill-creator quick_validate.py                        → Skill is valid!
Markdown 本地链接检查                                  → PASS
git diff --check                                      → PASS
```
