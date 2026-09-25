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


PAPER_FRAMEWORK = WORKSPACE_ROOT / "resources" / "templates" / "cumcm-paper-framework.tex"
FIGURE_SELECTION_TEMPLATE = WORKSPACE_ROOT / "resources" / "templates" / "figure-selection-record.md"
ARTIFACT_MAP_TEMPLATE = WORKSPACE_ROOT / "resources" / "templates" / "artifact-map.yaml"

BASE_FILES = {
    "00-admin/project.yaml": "project_id: {project_id}\ncontest: {contest}\nyear: {year}\nproblem: {problem}\nstatus: intake\nrandom_seed: 20260721\n",
    "00-admin/runbook.md": "# 运行手册\n\n> 按 `docs/standards/data-reproducibility.md` 维护。\n",
    "06-paper/references.bib": "",
    "08-delivery/file-list.md": "# 支撑材料文件清单\n\n> 按 `WG-RELEASE-001`、`PQA-RELEASE-001` 与 `OFFICIAL-CUMCM-001` 维护。\n",
    "sandbox/README.md": "# 实验区\n\n> 目录位置执行 `LAYOUT-001`；产物边界执行 `WG-TEST-001`；实验比较与采纳执行 `WG-MODEL-001`。\n",
}


def markdown_table(columns, row: dict[str, str] | None = None) -> str:
    header = "| " + " | ".join(columns) + " |\n"
    separator = "|" + "|".join("---" for _ in columns) + "|\n"
    if row is None:
        return header + separator
    values = "| " + " | ".join(row.get(column, "待填写") for column in columns) + " |\n"
    return header + separator + values


def learning_record(contracts) -> str:
    rows = "".join(
        "| "
        + " | ".join(
            {
                "item": f"sample-{index:02d}",
                "path_or_source": "resources/paper-library/待填写",
                "prohibited_copying": "待填写",
                "reviewed": "no",
            }.get(column, "待填写")
            for column in contracts.learning_sample_columns
        )
        + " |\n"
        for index in range(1, contracts.learning_paper_minimum + 1)
    )
    return (
        "# 写作前学习记录\n\n"
        f"- learning_status: `{contracts.learning_initial_status}`\n"
        "- completed_at: `YYYY-MM-DD`\n\n"
        "> 按 `PWL-GATE-001` 完成；门禁变化后以权威流程为准。\n\n"
        "## 赛题类型与各问写作重点\n\n"
        "记录赛题数学类型，并逐项说明 q01、q02 等子问题的写作重点。\n\n"
        "## 同类优秀论文\n\n"
        f"{markdown_table(contracts.learning_sample_columns)}"
        f"{rows}\n"
        "## 算法资料复核\n\n"
        f"{markdown_table(contracts.learning_algorithm_columns, {'question_id': 'q01', 'resource_path': 'resources/algorithm-library/待填写', 'status': 'pending'})}\n"
        "## 写作策略\n\n"
        "记录摘要、模型建立、结果分析、验证和图表叙事中可借鉴但不得复制的策略。\n"
    )


def project_files(contracts) -> dict[str, str]:
    problem_checklist = (
        "# 问题清单\n\n> 字段和维护要求执行 `docs/standards/workspace-governance.md` 第 3 节；表内登记要点，实质理由写在各节正文。\n\n"
        "## 题面与附件\n\n"
        + markdown_table(
            contracts.problem_attachment_columns,
            {"relative_file": "待填写", "exists": "no", "received_at": "YYYY-MM-DD"},
        )
        + "\n## 子问题\n\n"
        + markdown_table(
            contracts.problem_question_columns,
            {"question_id": "q01", "status": "draft"},
        )
        + "\n## 缺口与合规核对\n\n"
        + markdown_table(contracts.problem_risk_columns, {"rules_checked_at": "YYYY-MM-DD"})
    )
    model_selection = (
        "# 模型与算法选择记录\n\n"
        f"- selection_status: `{contracts.selection_initial_status}`\n"
        "- completed_at: `YYYY-MM-DD`\n\n"
        "> 按 `WG-MODEL-001` 完成；表内登记要点，实质理由写在各节正文。\n\n"
        + markdown_table(
            contracts.model_selection_columns,
            {
                "question_id": "q01",
                "library_resource": "resources/algorithm-library/待填写",
            },
        )
    )
    data_audit = (
        "# 数据审计\n\n"
        "> 记录要求执行 `docs/standards/data-reproducibility.md` §1.2；表内登记要点，实质说明写在各节正文。\n\n"
        "## 字段与范围\n\n"
        + markdown_table(["数据文件", "字段", "类型", "单位", "样本量", "时间范围", "空间范围"])
        + "\n## 质量问题\n\n"
        + markdown_table(["数据文件", "主键", "重复", "缺失", "异常", "非法编码", "数量级"])
        + "\n## 切分与泄漏\n\n"
        + markdown_table(["数据文件", "切分方式", "泄漏风险（时间/对象/空间/目标）", "核对结论"])
        + "\n## 处理与代码-输出映射\n\n"
        + markdown_table(["处理步骤", "规则", "处理前样本量", "处理后样本量", "受影响对象", "代码", "输出文件"])
    )
    ai_tool_log = (
        "# AI 工具实质使用台账\n\n> 按 `WG-AI-001` 维护。\n\n"
        + markdown_table(contracts.ai_log_columns)
    )
    return {
        **BASE_FILES,
        "01-problem/problem-checklist.md": problem_checklist,
        "02-data/data-audit.md": data_audit,
        "03-models/model-selection.md": model_selection,
        "00-admin/pre-writing-learning.md": learning_record(contracts),
        "05-evidence/evidence-index.csv": ",".join(contracts.claim_columns) + "\n",
        "05-evidence/literature-ledger.csv": ",".join(contracts.literature_columns) + "\n",
        "05-evidence/ai-tool-log.md": ai_tool_log,
        "07-review/review-log.md": "# 审稿记录\n\n> 字段语义执行 `PQA-REPORT-001`。\n\n" + markdown_table(contracts.review_log_columns),
    }


def figure_selection_record(contracts, project_id: str) -> str:
    text = FIGURE_SELECTION_TEMPLATE.read_text(encoding="utf-8").replace(
        "- project_id: `待填写`", f"- project_id: `{project_id}`", 1
    )
    registry = markdown_table(
        contracts.figure_registry_columns,
        {
            "figure_label": "`fig:q01-*`",
            "authoritative_source": "待填写",
            "generator": "待填写",
            "result_artifact": "`04-results/figures/...`",
            "paper_copy": "`06-paper/figures/...`",
            "final_pdf_page": "待定",
            "final_pdf_check": contracts.figure_initial_status,
        },
    ).rstrip()
    risk = markdown_table(contracts.figure_risk_columns).rstrip()
    return (
        text.replace("__FIGURE_REGISTRY_TABLE__", registry, 1)
        .replace("__FIGURE_RISK_TABLE__", risk, 1)
        .replace("__FIGURE_INITIAL_STATUS__", contracts.figure_initial_status, 1)
    )


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


def configure_utf8_stdio() -> None:
    """Keep console output UTF-8 on Windows terminals and redirected streams."""

    for stream in (sys.stdout, sys.stderr):
        reconfigure = getattr(stream, "reconfigure", None)
        if reconfigure is not None:
            try:
                reconfigure(encoding="utf-8", errors="replace")
            except (OSError, ValueError):
                pass


def main() -> int:
    configure_utf8_stdio()
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
    for template in (PAPER_FRAMEWORK, FIGURE_SELECTION_TEMPLATE, ARTIFACT_MAP_TEMPLATE):
        if not template.is_file():
            parser.error(f"missing project template: {template}")
    project_id = f"{contest}-{args.year}-{problem}"
    project = Path(args.root) / project_id
    if project.exists():
        parser.error(f"refusing to overwrite existing project: {project}")

    for item in contracts.recommended_project_directories:
        (project / item).mkdir(parents=True, exist_ok=False)
    values = {"project_id": project_id, "contest": contest, "year": args.year, "problem": problem}
    for relative, content in project_files(contracts).items():
        target = project / relative
        target.write_text(content.format(**values), encoding="utf-8", newline="\n")
    figure_selection_text = figure_selection_record(contracts, project_id)
    (project / "00-admin/figure-selection-record.md").write_text(
        figure_selection_text, encoding="utf-8", newline="\n"
    )
    artifact_map_text = ARTIFACT_MAP_TEMPLATE.read_text(encoding="utf-8").replace(
        "__PROJECT_ID__", project_id, 1
    )
    (project / "00-admin/artifact-map.yaml").write_text(
        artifact_map_text, encoding="utf-8", newline="\n"
    )
    shutil.copyfile(PAPER_FRAMEWORK, project / "06-paper/main.tex")
    print(f"Created {project.resolve()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
