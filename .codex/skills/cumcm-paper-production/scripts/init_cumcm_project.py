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
    "01-problem/problem-checklist.md": "# 问题清单\n\n| question_id | task | inputs | outputs | constraints | metric | status |\n|---|---|---|---|---|---|---|\n| q01 | 待填写 | 待填写 | 待填写 | 待填写 | 待填写 | draft |\n",
    "05-evidence/evidence-index.csv": "claim_id,question_id,claim,evidence_type,source_path,generator,generated_at,status\n",
    "05-evidence/literature-ledger.csv": "citation_key,title,authors,year,doi_or_url,retrieved_at,used_in,verified\n",
    "05-evidence/ai-tool-log.md": "# AI 工具使用台账\n\n按日期记录工具/版本、目的、关键交互、采纳内容和人工修改。发布时据此生成“AI 工具使用详情”PDF。\n",
    "06-paper/main.tex": "% 仅从 verified 证据写入具体数值。正式模板按当年竞赛要求配置。\n",
    "06-paper/references.bib": "",
    "07-review/review-log.md": "# 审稿记录\n\n| date | reviewer | severity | location | finding | evidence | resolution |\n|---|---|---|---|---|---|---|\n",
    "07-review/paper-quality-audit.md": "# 论文质量审查报告\n\n> 按 `docs/standards/paper-quality-audit.md` 审查最终 PDF；论文或图表变更后必须更新本报告。\n\n## 机器可读门禁\n\n- audit_date: `待填写`\n- final_pdf: `08-delivery/paper.pdf`\n- final_pdf_sha256: `待填写`\n- paper_writing_compliance: `BLOCKED`\n- national_award_competitiveness: `待审查`\n- full_pdf_render_review: `BLOCKED`\n- figure_clarity_and_intuitiveness: `BLOCKED`\n- overlap_and_clipping: `BLOCKED`\n- flowchart_logic: `BLOCKED`\n- open_critical: `0`\n- open_major: `0`\n- open_presentation_minor: `0`\n- release_decision: `BLOCKED`\n\n## 一、结论\n\n待填写。\n\n## 二、硬性合规矩阵\n\n待填写。\n\n## 三、国奖竞争力评分\n\n待填写。\n\n## 四、图表逐项审查\n\n待填写。\n\n## 五、发现项\n\n待填写。\n\n## 六、最终判定依据与免责声明\n\n本结论是内部竞争力预审，不构成官方获奖保证。\n",
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
