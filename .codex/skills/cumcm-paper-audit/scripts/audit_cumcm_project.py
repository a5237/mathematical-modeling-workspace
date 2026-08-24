#!/usr/bin/env python3
"""Static release gate for normalized CUMCM projects."""

from __future__ import annotations

import argparse
import csv
import hashlib
import re
import sys
from pathlib import Path

WORKSPACE_ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(WORKSPACE_ROOT / "tools"))

from control_contracts import ContractError, load_workspace_contracts


REQUIRED_DIRS = ["00-admin", "01-problem", "02-data/raw", "03-models", "04-results", "05-evidence", "06-paper", "07-review", "08-delivery"]
REQUIRED_FILES = ["00-admin/project.yaml", "01-problem/problem-checklist.md", "05-evidence/evidence-index.csv", "05-evidence/literature-ledger.csv", "05-evidence/ai-tool-log.md", "06-paper/main.tex", "07-review/review-log.md", "08-delivery/file-list.md"]
RELEASE_REQUIRED_FILES = [
    "00-admin/pre-writing-learning.md",
    "03-models/model-selection.md",
    "07-review/paper-quality-audit.md",
]
PLACEHOLDER = re.compile(r"TODO|TBD|FIXME|待填写|待补|占位|XX+", re.IGNORECASE)
QUALITY_FIELD = re.compile(r"^\s*-\s*([a-z0-9_]+):\s*`([^`]*)`\s*$", re.MULTILINE)


def audit_workflow_gate(
    root: Path,
    relative: str,
    status_key: str,
    expected_status: str,
    minimum_learning_papers: int,
    errors: list[str],
) -> None:
    path = root / relative
    if not path.is_file():
        return
    text = path.read_text(encoding="utf-8", errors="replace")
    fields = dict(QUALITY_FIELD.findall(text))
    if fields.get(status_key) != expected_status:
        errors.append(f"MAJOR workflow gate {relative}: {status_key} must be {expected_status}")
    completed_at = fields.get("completed_at", "")
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", completed_at):
        errors.append(f"MAJOR workflow gate {relative}: completed_at must use YYYY-MM-DD")
    if PLACEHOLDER.search(text):
        errors.append(f"MAJOR unresolved placeholder in {relative}")

    table_lines = text.splitlines()
    checklist_path = root / "01-problem/problem-checklist.md"
    checklist_text = checklist_path.read_text(encoding="utf-8", errors="replace") if checklist_path.is_file() else ""
    expected_questions = set(re.findall(r"^\|\s*(q\d+)\s*\|", checklist_text, re.MULTILINE))
    if status_key == "learning_status":
        sample_rows = [
            [cell.strip() for cell in line.strip().strip("|").split("|")]
            for line in table_lines
            if re.match(r"^\|\s*sample-\d+\s*\|", line)
        ]
        reviewed_rows = [
            cells
            for cells in sample_rows
            if len(cells) >= 6
            and cells[1].replace("\\", "/").startswith("resources/paper-library/")
            and cells[-1].lower() in {"yes", "true", "1"}
        ]
        if len(reviewed_rows) < minimum_learning_papers:
            errors.append(
                f"MAJOR workflow gate {relative}: fewer than {minimum_learning_papers} reviewed same-type papers from resources/paper-library"
            )
        learned_questions = set(re.findall(r"^\|\s*(q\d+)\s*\|", text, re.MULTILINE))
        missing_learning = sorted(expected_questions - learned_questions)
        if missing_learning:
            errors.append(f"MAJOR workflow gate {relative}: missing algorithm review for {missing_learning}")
    elif status_key == "selection_status":
        selection_rows = [
            [cell.strip() for cell in line.strip().strip("|").split("|")]
            for line in table_lines
            if re.match(r"^\|\s*q\d+\s*\|", line)
        ]
        if not selection_rows:
            errors.append(f"MAJOR workflow gate {relative}: no subproblem selection record")
        elif any(
            len(cells) < 3 or not cells[2].replace("\\", "/").startswith("resources/algorithm-library/")
            for cells in selection_rows
        ):
            errors.append(f"MAJOR workflow gate {relative}: subproblem row missing algorithm-library resource path")
        selected_questions = {cells[0] for cells in selection_rows if cells}
        missing_selection = sorted(expected_questions - selected_questions)
        if missing_selection:
            errors.append(f"MAJOR workflow gate {relative}: missing model selection for {missing_selection}")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def audit_quality_report(
    root: Path,
    delivery_pdf: Path | None,
    contracts,
    errors: list[str],
) -> None:
    path = root / "07-review/paper-quality-audit.md"
    if not path.is_file():
        return
    text = path.read_text(encoding="utf-8", errors="replace")
    fields = dict(QUALITY_FIELD.findall(text))
    missing = sorted(set(contracts.quality_field_options) - fields.keys())
    if missing:
        errors.append(f"MAJOR {path}: missing quality-gate fields {missing}")
        return
    if PLACEHOLDER.search(text):
        errors.append("MAJOR unresolved placeholder in 07-review/paper-quality-audit.md")

    expected: dict[str, set[str]] = {}
    for key, options in contracts.quality_field_options.items():
        if key.startswith("open_"):
            expected[key] = {"0"}
        elif key == "national_award_competitiveness":
            expected[key] = set(options)
        elif key == "release_decision":
            expected[key] = {"READY"}
        elif "PASS" in options:
            expected[key] = {value for value in options if value in {"PASS", "NOT_APPLICABLE"}}
    for key, allowed in expected.items():
        if fields[key] not in allowed:
            errors.append(f"MAJOR quality gate {key}: expected {sorted(allowed)}, found {fields[key]!r}")

    integer_limits = {
        "body_word_count": (contracts.body_word_minimum, None),
        "body_page_count": (contracts.body_page_minimum, contracts.body_page_maximum),
        "body_figure_count": (contracts.body_figure_minimum, None),
        "body_table_count": (contracts.body_table_minimum, None),
    }
    parsed_counts: dict[str, int] = {}
    for key, (minimum, maximum) in integer_limits.items():
        try:
            value = int(fields[key])
        except ValueError:
            errors.append(f"MAJOR quality gate {key} must be an integer")
            continue
        parsed_counts[key] = value
        if value < minimum or (maximum is not None and value > maximum):
            expected_range = f">= {minimum}" if maximum is None else f"{minimum}..{maximum}"
            errors.append(f"MAJOR quality gate {key}: expected {expected_range}, found {value}")

    page_range = re.fullmatch(r"\s*(\d+)\s*[-–—]\s*(\d+)\s*", fields["body_page_range"])
    if page_range is None:
        errors.append("MAJOR quality gate body_page_range must use <start>-<end>")
    else:
        start_page, end_page = map(int, page_range.groups())
        if end_page < start_page:
            errors.append("MAJOR quality gate body_page_range ends before it starts")
        elif "body_page_count" in parsed_counts and end_page - start_page + 1 != parsed_counts["body_page_count"]:
            errors.append("MAJOR quality gate body_page_range does not match body_page_count")

    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", fields["audit_date"]):
        errors.append("MAJOR quality gate audit_date must use YYYY-MM-DD")
    if not re.fullmatch(r"[0-9a-fA-F]{64}", fields["final_pdf_sha256"]):
        errors.append("MAJOR quality gate final_pdf_sha256 must contain 64 hexadecimal characters")

    relative_pdf = Path(fields["final_pdf"])
    if relative_pdf.is_absolute() or ".." in relative_pdf.parts:
        errors.append("CRITICAL quality gate final_pdf is unsafe")
        return
    reported_pdf = (root / relative_pdf).resolve()
    try:
        reported_pdf.relative_to(root)
    except ValueError:
        errors.append("CRITICAL quality gate final_pdf escapes the project root")
        return
    if not reported_pdf.is_file():
        errors.append(f"CRITICAL quality gate final_pdf does not exist: {relative_pdf}")
        return
    if delivery_pdf is not None and reported_pdf != delivery_pdf.resolve():
        errors.append("MAJOR quality gate final_pdf is not the sole delivery PDF")
    actual_hash = sha256(reported_pdf)
    if fields["final_pdf_sha256"].lower() != actual_hash:
        errors.append("CRITICAL quality gate PDF hash does not match the reviewed delivery PDF")


def read_csv(path: Path, required: set[str], errors: list[str]) -> list[dict[str, str]]:
    try:
        with path.open(encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            fields = set(reader.fieldnames or [])
            if not required.issubset(fields):
                errors.append(f"MAJOR {path}: missing columns {sorted(required - fields)}")
            return list(reader)
    except Exception as exc:
        errors.append(f"CRITICAL {path}: cannot parse CSV: {exc}")
        return []


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("project", type=Path)
    parser.add_argument("--phase", choices=("draft", "release"), default="draft")
    args = parser.parse_args()
    root = args.project.resolve()
    errors: list[str] = []

    try:
        contracts = load_workspace_contracts(WORKSPACE_ROOT)
    except ContractError as exc:
        print(f"CRITICAL authority contract: {exc}")
        return 2

    if not root.is_dir():
        parser.error(f"project does not exist: {root}")
    for relative in REQUIRED_DIRS:
        if not (root / relative).is_dir():
            errors.append(f"MAJOR missing directory: {relative}")
    for relative in REQUIRED_FILES:
        if not (root / relative).is_file():
            errors.append(f"MAJOR missing file: {relative}")
    if args.phase == "release":
        for relative in RELEASE_REQUIRED_FILES:
            if not (root / relative).is_file():
                errors.append(f"MAJOR missing release file: {relative}")
        audit_workflow_gate(
            root,
            "03-models/model-selection.md",
            "selection_status",
            contracts.selection_complete_status,
            contracts.learning_paper_minimum,
            errors,
        )
        audit_workflow_gate(
            root,
            "00-admin/pre-writing-learning.md",
            "learning_status",
            contracts.learning_complete_status,
            contracts.learning_paper_minimum,
            errors,
        )

    evidence_path = root / "05-evidence/evidence-index.csv"
    if evidence_path.is_file():
        rows = read_csv(evidence_path, set(contracts.claim_columns), errors)
        if args.phase == "release" and not rows:
            errors.append("CRITICAL evidence index has no claims")
        for line, row in enumerate(rows, 2):
            source = row.get("source_path", "").strip()
            status = row.get("status", "").strip().lower()
            if status not in contracts.evidence_statuses:
                errors.append(f"MAJOR evidence row {line}: invalid status {status!r}")
            if not source or Path(source).is_absolute() or ".." in Path(source).parts:
                errors.append(f"CRITICAL evidence row {line}: unsafe or missing source_path")
            elif not (root / source).is_file():
                errors.append(f"CRITICAL evidence row {line}: missing artifact {source}")

    literature_path = root / "05-evidence/literature-ledger.csv"
    if literature_path.is_file():
        rows = read_csv(literature_path, set(contracts.literature_columns), errors)
        for line, row in enumerate(rows, 2):
            if args.phase == "release" and row.get("verified", "").strip().lower() not in {"yes", "true", "1"}:
                errors.append(f"MAJOR literature row {line}: source not verified")
            locator = row.get("doi_or_url", "").strip()
            if locator and not (locator.startswith("http://") or locator.startswith("https://") or locator.startswith("10.")):
                errors.append(f"MAJOR literature row {line}: invalid DOI/URL")

    for relative in ("01-problem/problem-checklist.md", "06-paper/main.tex", "08-delivery/file-list.md"):
        path = root / relative
        if path.is_file() and args.phase == "release" and PLACEHOLDER.search(path.read_text(encoding="utf-8", errors="replace")):
            errors.append(f"MAJOR unresolved placeholder in {relative}")

    pdfs = list((root / "08-delivery").glob("*.pdf")) if (root / "08-delivery").is_dir() else []
    if args.phase == "release":
        if len(pdfs) != 1:
            errors.append(f"MAJOR delivery must contain exactly one PDF, found {len(pdfs)}")
        elif pdfs[0].stat().st_size > contracts.paper_maximum_bytes:
            errors.append("CRITICAL delivery PDF exceeds OFFICIAL-CUMCM-001 size limit")
        audit_quality_report(root, pdfs[0] if len(pdfs) == 1 else None, contracts, errors)

    print(f"Audit root: {root}")
    if errors:
        print("BLOCKED")
        for item in errors:
            print(f"- {item}")
        return 1
    print("PASS (static evidence contract; quality-report assertions still require independent human review)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
