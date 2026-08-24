#!/usr/bin/env python3
"""Create a normalized, evidence-driven CUMCM project without overwriting files."""

from __future__ import annotations

import argparse
import re
import shutil
import sys
from pathlib import Path

WORKSPACE_ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(WORKSPACE_ROOT / "tools"))

from control_contracts import ContractError, load_workspace_contracts


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

PAPER_FRAMEWORK = WORKSPACE_ROOT / "resources" / "templates" / "cumcm-paper-framework.tex"
FIGURE_SELECTION_TEMPLATE = WORKSPACE_ROOT / "resources" / "templates" / "figure-selection-record.md"

BASE_FILES = {
    "00-admin/project.yaml": "project_id: {project_id}\ncontest: {contest}\nyear: {year}\nproblem: {problem}\nstatus: intake\nrandom_seed: 20260721\n",
    "00-admin/runbook.md": "# 运行手册\n\n记录环境、入口命令、参数、随机种子和预期输出。\n",
    "01-problem/problem-checklist.md": "# 问题清单\n\n| question_id | task | inputs | outputs | constraints | metric | status |\n|---|---|---|---|---|---|---|\n| q01 | 待填写 | 待填写 | 待填写 | 待填写 | 待填写 | draft |\n",
    "03-models/model-selection.md": "# 模型与算法选择记录\n\n- selection_status: `INCOMPLETE`\n- completed_at: `YYYY-MM-DD`\n\n> 按 `docs/standards/workspace-governance.md` 的 `WG-MODEL-001` 完成；本记录不另行定义模型数量或偏离规则。\n\n| question_id | problem_features | library_resource | candidates | suitability_checks | selected_model | deviation_reason | baseline | validation_plan |\n|---|---|---|---|---|---|---|---|---|\n| q01 | 待填写 | resources/algorithm-library/待填写 | 待填写 | 目标、假设、数据、规模、约束、依赖、指标 | 待填写 | 不适用时写无 | 待填写 | 待填写 |\n",
    "05-evidence/ai-tool-log.md": "# AI 工具使用台账\n\n按日期记录工具/版本、目的、关键交互、采纳内容和人工修改；发布文件执行 `OFFICIAL-CUMCM-001`。\n",
    "06-paper/references.bib": "",
    "08-delivery/file-list.md": "# 支撑材料文件清单\n\n发布前列出每个文件、用途及其对应论文位置。\n",
}


def learning_record(contracts) -> str:
    rows = "\n".join(
        f"| sample-{index:02d} | resources/paper-library/待填写 | 待填写 | 待填写 | 原文、公式、数据、图表、结论 | no |"
        for index in range(1, contracts.learning_paper_minimum + 1)
    )
    return (
        "# 写作前学习记录\n\n"
        "- learning_status: `INCOMPLETE`\n"
        "- completed_at: `YYYY-MM-DD`\n\n"
        "> 按 `PWL-GATE-001` 完成；门禁变化后以权威流程为准。\n\n"
        "## 同类优秀论文\n\n"
        "| item | path_or_source | problem_type | structural_lessons | prohibited_copying | reviewed |\n"
        "|---|---|---|---|---|---|\n"
        f"{rows}\n\n"
        "## 算法资料复核\n\n"
        "| question_id | resource_path | definition_and_assumptions | applicability | code_review | status |\n"
        "|---|---|---|---|---|---|\n"
        "| q01 | resources/algorithm-library/待填写 | 待填写 | 待填写 | 待填写 | pending |\n\n"
        "## 写作策略\n\n"
        "记录摘要、模型建立、结果分析、验证和图表叙事中可借鉴但不得复制的策略。\n"
    )


def quality_report(contracts) -> str:
    def initialize(match: re.Match) -> str:
        key = match.group(2)
        options = contracts.quality_field_options[key]
        value = (
            "0" if key.startswith("open_")
            else options[0] if key == "final_pdf" and options
            else "待审查" if key == "national_award_competitiveness"
            else "BLOCKED" if {"PASS", "READY"} & set(options)
            else "待填写"
        )
        return f"{match.group(1)} `{value}`"

    return re.sub(r"^(- ([a-z0-9_]+):)\s*.*$", initialize, contracts.quality_report_template, flags=re.MULTILINE).rstrip() + "\n"


def project_files(contracts) -> dict[str, str]:
    review_header = "| " + " | ".join(contracts.quality_finding_fields) + " |\n"
    review_separator = "|" + "|".join("---" for _ in contracts.quality_finding_fields) + "|\n"
    return {
        **BASE_FILES,
        "00-admin/pre-writing-learning.md": learning_record(contracts),
        "05-evidence/evidence-index.csv": ",".join(contracts.claim_columns) + "\n",
        "05-evidence/literature-ledger.csv": ",".join(contracts.literature_columns) + "\n",
        "07-review/review-log.md": "# 审稿记录\n\n" + review_header + review_separator,
        "07-review/paper-quality-audit.md": quality_report(contracts),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default="workspace/projects")
    parser.add_argument("--contest", default="cumcm")
    parser.add_argument("--year", type=int, required=True)
    parser.add_argument("--problem", required=True)
    args = parser.parse_args()

    try:
        contracts = load_workspace_contracts(WORKSPACE_ROOT)
    except ContractError as exc:
        parser.error(f"invalid authority contract: {exc}")

    contest = args.contest.lower()
    problem = args.problem.lower()
    if not re.fullmatch(r"[a-z0-9-]+", contest) or not re.fullmatch(r"[a-z0-9-]+", problem):
        parser.error("contest and problem must use lowercase ASCII letters, digits, or hyphens")
    for template in (PAPER_FRAMEWORK, FIGURE_SELECTION_TEMPLATE):
        if not template.is_file():
            parser.error(f"missing project template: {template}")
    project_id = f"{contest}-{args.year}-{problem}"
    project = Path(args.root) / project_id
    if project.exists():
        parser.error(f"refusing to overwrite existing project: {project}")

    for item in DIRS:
        (project / item).mkdir(parents=True, exist_ok=False)
    values = {"project_id": project_id, "contest": contest, "year": args.year, "problem": problem}
    for relative, content in project_files(contracts).items():
        target = project / relative
        target.write_text(content.format(**values), encoding="utf-8", newline="\n")
    figure_selection_text = FIGURE_SELECTION_TEMPLATE.read_text(encoding="utf-8").replace(
        "- project_id: `待填写`", f"- project_id: `{project_id}`", 1
    )
    (project / "00-admin/figure-selection-record.md").write_text(
        figure_selection_text, encoding="utf-8", newline="\n"
    )
    shutil.copyfile(PAPER_FRAMEWORK, project / "06-paper/main.tex")
    print(f"Created {project.resolve()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
