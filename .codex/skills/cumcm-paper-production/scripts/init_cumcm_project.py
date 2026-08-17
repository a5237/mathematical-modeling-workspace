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
