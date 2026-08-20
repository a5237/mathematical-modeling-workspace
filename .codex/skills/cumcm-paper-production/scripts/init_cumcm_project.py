#!/usr/bin/env python3
"""Create a normalized, evidence-driven CUMCM project without overwriting files."""

from __future__ import annotations

import argparse
import re
from pathlib import Path


DIRS = (
    "00-admin",
    "01-problem/attachments",
    "02-data/raw",
    "02-data/processed",
    "03-models/q01",
    "04-results/tables",
    "04-results/figures",
    "04-results/metrics",
    "04-results/logs",
    "05-evidence",
    "06-paper/figures",
    "06-paper/tables",
    "07-review",
    "08-delivery/support-materials",
)

FILES = {
    "00-admin/project.yaml": "project_id: {project_id}\ncontest: {contest}\nyear: {year}\nproblem: {problem}\nstatus: intake\nrandom_seed: 20260721\n",
    "00-admin/runbook.md": "# 运行手册\n\n记录环境、入口命令、参数、随机种子和预期输出。\n",
    "00-admin/pre-writing-learning.md": "# 写作前学习记录\n\n- learning_status: `INCOMPLETE`\n- completed_at: `YYYY-MM-DD`\n\n> 按 `docs/guides/pre-writing-learning.md` 完成。主要模型、算法或论文结构变化后须重新确认。\n\n## 同类优秀论文\n\n| item | path_or_source | problem_type | structural_lessons | prohibited_copying | reviewed |\n|---|---|---|---|---|---|\n| sample-01 | resources/paper-library/待填写 | 待填写 | 待填写 | 原文、公式、数据、图表、结论 | no |\n| sample-02 | resources/paper-library/待填写 | 待填写 | 待填写 | 原文、公式、数据、图表、结论 | no |\n\n## 算法资料复核\n\n| question_id | resource_path | definition_and_assumptions | applicability | code_review | status |\n|---|---|---|---|---|---|\n| q01 | resources/algorithm-library/待填写 | 待填写 | 待填写 | 待填写 | pending |\n\n## 写作策略\n\n记录摘要、模型建立、结果分析、验证和图表叙事中可借鉴但不得复制的策略。\n",
    "01-problem/problem-checklist.md": "# 问题清单\n\n| question_id | task | inputs | outputs | constraints | metric | status |\n|---|---|---|---|---|---|---|\n| q01 | 待填写 | 待填写 | 待填写 | 待填写 | 待填写 | draft |\n",
    "03-models/model-selection.md": "# 模型与算法选择记录\n\n- selection_status: `INCOMPLETE`\n- completed_at: `YYYY-MM-DD`\n\n> 按 `docs/standards/workspace-governance.md` 的 `WG-MODEL-001` 完成；本记录不另行定义模型数量或偏离规则。\n\n| question_id | problem_features | library_resource | candidates | suitability_checks | selected_model | deviation_reason | baseline | validation_plan |\n|---|---|---|---|---|---|---|---|---|\n| q01 | 待填写 | resources/algorithm-library/待填写 | 待填写 | 目标、假设、数据、规模、约束、依赖、指标 | 待填写 | 不适用时写无 | 待填写 | 待填写 |\n",
    "05-evidence/evidence-index.csv": "claim_id,question_id,claim,evidence_type,source_path,generator,generated_at,status\n",
    "05-evidence/literature-ledger.csv": "citation_key,title,authors,year,doi_or_url,retrieved_at,used_in,verified\n",
    "05-evidence/ai-tool-log.md": "# AI 工具使用台账\n\n按日期记录工具/版本、目的、关键交互、采纳内容和人工修改。发布时按 `OFFICIAL-CUMCM-001` 据此生成 `AI 工具使用详情.pdf`。\n",
    "06-paper/main.tex": "% 仅从 verified 证据写入具体数值。正式模板按当年竞赛要求配置。\n",
    "06-paper/references.bib": "",
    "07-review/review-log.md": "# 审稿记录\n\n| date | reviewer | severity | location | finding | evidence | resolution |\n|---|---|---|---|---|---|---|\n",
    "07-review/paper-quality-audit.md": "# 论文质量审查报告\n\n> 按 `docs/standards/paper-quality-audit.md` 的 `PQA-REPORT-001` 审查最终 PDF；论文或图表变更后必须更新本报告。\n\n## 机器可读门禁\n\n- audit_date: `待填写`\n- final_pdf: `08-delivery/paper.pdf`\n- final_pdf_sha256: `待填写`\n- body_word_count: `待填写`\n- body_page_range: `待填写`\n- body_page_count: `待填写`\n- body_figure_count: `待填写`\n- body_table_count: `待填写`\n- body_length_and_visual_count_gate: `BLOCKED`\n- paper_writing_compliance: `BLOCKED`\n- national_award_competitiveness: `待审查`\n- full_pdf_render_review: `BLOCKED`\n- figure_clarity_and_intuitiveness: `BLOCKED`\n- overlap_and_clipping: `BLOCKED`\n- flowchart_logic: `BLOCKED`\n- open_critical: `0`\n- open_major: `0`\n- open_presentation_minor: `0`\n- release_decision: `BLOCKED`\n\n## 一、结论\n\n待填写。\n\n## 二、硬性合规矩阵\n\n待填写。\n\n## 三、国奖竞争力评分\n\n待填写。\n\n## 四、图表逐项审查\n\n待填写。\n\n## 五、发现项\n\n待填写。\n\n## 六、最终判定依据与免责声明\n\n本结论是内部竞争力预审，不构成官方获奖保证。\n",
    "08-delivery/file-list.md": "# 支撑材料文件清单\n\n发布前列出每个文件、用途及其对应论文位置。\n",
}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default="workspace/projects")
    parser.add_argument("--contest", default="cumcm")
    parser.add_argument("--year", type=int, required=True)
    parser.add_argument("--problem", required=True)
    args = parser.parse_args()

    contest = args.contest.lower()
    problem = args.problem.lower()
    if not re.fullmatch(r"[a-z0-9-]+", contest) or not re.fullmatch(r"[a-z0-9-]+", problem):
        parser.error("contest and problem must use lowercase ASCII letters, digits, or hyphens")
    project_id = f"{contest}-{args.year}-{problem}"
    project = Path(args.root) / project_id
    if project.exists():
        parser.error(f"refusing to overwrite existing project: {project}")

    for item in DIRS:
        (project / item).mkdir(parents=True, exist_ok=False)
    values = {"project_id": project_id, "contest": contest, "year": args.year, "problem": problem}
    for relative, content in FILES.items():
        target = project / relative
        target.write_text(content.format(**values), encoding="utf-8", newline="\n")
    print(f"Created {project.resolve()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
