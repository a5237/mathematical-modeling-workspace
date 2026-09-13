#!/usr/bin/env python3
"""Create a recommended evidence-driven CUMCM project without overwriting files."""

from __future__ import annotations

import argparse
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
    "01-problem/problem-checklist.md": (
        "# 问题清单\n\n"
        "## 题面与附件\n\n"
        "| relative_file | exists | source | received_at |\n"
        "|---|---|---|---|\n"
        "| 待填写 | no | 待填写 | YYYY-MM-DD |\n\n"
        "> 中间门禁只登记关键文件名与存在状态，不记录文件哈希。\n\n"
        "## 子问题\n\n"
        "| question_id | task | inputs | outputs | constraints | metric | status |\n"
        "|---|---|---|---|---|---|---|\n"
        "| q01 | 待填写 | 待填写 | 待填写 | 待填写 | 待填写 | draft |\n"
    ),
    "03-models/model-selection.md": "# 模型与算法选择记录\n\n- selection_status: `INCOMPLETE`\n- completed_at: `YYYY-MM-DD`\n\n> 按 `docs/standards/workspace-governance.md` 的 `WG-MODEL-001` 完成；本记录不另行定义模型数量或偏离规则。\n\n| question_id | problem_features | library_resource | candidates | suitability_checks | selected_model | deviation_reason | baseline | validation_plan |\n|---|---|---|---|---|---|---|---|---|\n| q01 | 待填写 | resources/algorithm-library/待填写 | 待填写 | 目标、假设、数据、规模、约束、依赖、指标 | 待填写 | 不适用时写无 | 待填写 | 待填写 |\n",
    "05-evidence/ai-tool-log.md": (
        "# AI 工具实质使用台账\n\n"
        "> 只登记对模型、代码、论文或正式交付有实质影响的使用；普通问答、微小措辞调整和无实质影响的交互无需逐条记录。\n\n"
        "| date | tool_and_model | stage | material_prompt_or_method | adopted_content | human_changes | verification |\n"
        "|---|---|---|---|---|---|---|\n"
    ),
    "06-paper/references.bib": "",
    "08-delivery/file-list.md": "# 支撑材料文件清单\n\n发布前列出每个文件、用途及其对应论文位置。\n",
}

REVIEW_FIELDS = (
    "id",
    "severity",
    "location",
    "criterion",
    "finding",
    "evidence",
    "required_fix",
    "verification",
    "status",
)


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
        "## 赛题类型与各问写作重点\n\n"
        "记录赛题数学类型，并逐项说明 q01、q02 等子问题的写作重点。\n\n"
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


def project_files(contracts) -> dict[str, str]:
    review_header = "| " + " | ".join(REVIEW_FIELDS) + " |\n"
    review_separator = "|" + "|".join("---" for _ in REVIEW_FIELDS) + "|\n"
    return {
        **BASE_FILES,
        "00-admin/pre-writing-learning.md": learning_record(contracts),
        "05-evidence/evidence-index.csv": ",".join(contracts.claim_columns) + "\n",
        "05-evidence/literature-ledger.csv": ",".join(contracts.literature_columns) + "\n",
        "07-review/review-log.md": "# 审稿记录\n\n" + review_header + review_separator,
    }


def safe_path_component(value: str, label: str, parser: argparse.ArgumentParser) -> str:
    """Reject only values that cannot safely form one filesystem path segment."""

    value = value.strip()
    forbidden = '<>:"/\\|?*'
    reserved = {
        "CON", "PRN", "AUX", "NUL",
        *(f"COM{index}" for index in range(1, 10)),
        *(f"LPT{index}" for index in range(1, 10)),
    }
    if (
        not value
        or value in {".", ".."}
        or any(character in value for character in forbidden)
        or any(ord(character) < 32 for character in value)
        or value.endswith((" ", "."))
        or value.split(".", 1)[0].upper() in reserved
    ):
        parser.error(f"{label} cannot be represented as a safe path component")
    return value.lower()


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

    contest = safe_path_component(args.contest, "contest", parser)
    problem = safe_path_component(args.problem, "problem", parser)
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
