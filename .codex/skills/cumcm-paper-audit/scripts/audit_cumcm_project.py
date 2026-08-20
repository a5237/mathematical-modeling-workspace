#!/usr/bin/env python3
"""Static release gate for normalized CUMCM projects."""

from __future__ import annotations

import argparse
import csv
import hashlib
import re
import sys
from pathlib import Path


REQUIRED_DIRS = ["00-admin", "01-problem", "02-data/raw", "03-models", "04-results", "05-evidence", "06-paper", "07-review", "08-delivery"]
REQUIRED_FILES = ["00-admin/project.yaml", "01-problem/problem-checklist.md", "05-evidence/evidence-index.csv", "05-evidence/literature-ledger.csv", "05-evidence/ai-tool-log.md", "06-paper/main.tex", "07-review/review-log.md", "08-delivery/file-list.md"]
RELEASE_REQUIRED_FILES = [
    "00-admin/pre-writing-learning.md",
    "03-models/model-selection.md",
    "07-review/paper-quality-audit.md",
]
PLACEHOLDER = re.compile(r"TODO|TBD|FIXME|待填写|待补|占位|XX+", re.IGNORECASE)
QUALITY_FIELD = re.compile(r"^\s*-\s*([a-z0-9_]+):\s*`([^`]*)`\s*$", re.MULTILINE)
CLAIM_COLUMNS = {"claim_id", "question_id", "claim", "evidence_type", "source_path", "generator", "generated_at", "status"}
LIT_COLUMNS = {"citation_key", "title", "authors", "year", "doi_or_url", "retrieved_at", "used_in", "verified"}
QUALITY_REQUIRED_FIELDS = {
    "audit_date",
    "final_pdf",
    "final_pdf_sha256",
    "body_word_count",
    "body_page_range",
    "body_page_count",
    "body_figure_count",
    "body_table_count",
    "body_length_and_visual_count_gate",
    "paper_writing_compliance",
    "national_award_competitiveness",
    "full_pdf_render_review",
    "figure_clarity_and_intuitiveness",
    "overlap_and_clipping",
    "flowchart_logic",
    "open_critical",
    "open_major",
    "open_presentation_minor",
    "release_decision",
}


def audit_workflow_gate(root: Path, relative: str, status_key: str, errors: list[str]) -> None:
    path = root / relative
    if not path.is_file():
        return
    text = path.read_text(encoding="utf-8", errors="replace")
    fields = dict(QUALITY_FIELD.findall(text))
    if fields.get(status_key) != "COMPLETE":
        errors.append(f"MAJOR workflow gate {relative}: {status_key} must be COMPLETE")
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
        if len(reviewed_rows) < 2:
            errors.append(
                f"MAJOR workflow gate {relative}: fewer than two reviewed same-type papers from resources/paper-library"
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


def audit_quality_report(root: Path, delivery_pdf: Path | None, errors: list[str]) -> None:
    path = root / "07-review/paper-quality-audit.md"
    if not path.is_file():
        return
    text = path.read_text(encoding="utf-8", errors="replace")
    fields = dict(QUALITY_FIELD.findall(text))
    missing = sorted(QUALITY_REQUIRED_FIELDS - fields.keys())
    if missing:
        errors.append(f"MAJOR {path}: missing quality-gate fields {missing}")
        return
    if PLACEHOLDER.search(text):
        errors.append("MAJOR unresolved placeholder in 07-review/paper-quality-audit.md")

    expected = {
        "body_length_and_visual_count_gate": {"PASS"},
        "paper_writing_compliance": {"PASS"},
        "national_award_competitiveness": {
            "MEETS_NATIONAL_AWARD_COMPETITIVE_STANDARD",
            "DOES_NOT_MEET_NATIONAL_AWARD_COMPETITIVE_STANDARD",
        },
        "full_pdf_render_review": {"PASS"},
        "figure_clarity_and_intuitiveness": {"PASS"},
        "overlap_and_clipping": {"PASS"},
        "flowchart_logic": {"PASS", "NOT_APPLICABLE"},
        "open_critical": {"0"},
        "open_major": {"0"},
        "open_presentation_minor": {"0"},
        "release_decision": {"READY"},
    }
    for key, allowed in expected.items():
        if fields[key] not in allowed:
            errors.append(f"MAJOR quality gate {key}: expected {sorted(allowed)}, found {fields[key]!r}")

    integer_limits = {
        "body_word_count": (15000, None),
        "body_page_count": (20, 30),
        "body_figure_count": (5, None),
        "body_table_count": (3, None),
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
        audit_workflow_gate(root, "03-models/model-selection.md", "selection_status", errors)
        audit_workflow_gate(root, "00-admin/pre-writing-learning.md", "learning_status", errors)

    evidence_path = root / "05-evidence/evidence-index.csv"
    if evidence_path.is_file():
        rows = read_csv(evidence_path, CLAIM_COLUMNS, errors)
        if args.phase == "release" and not rows:
            errors.append("CRITICAL evidence index has no claims")
        for line, row in enumerate(rows, 2):
            source = row.get("source_path", "").strip()
            status = row.get("status", "").strip().lower()
            if status not in {"draft", "verified", "rejected"}:
                errors.append(f"MAJOR evidence row {line}: invalid status {status!r}")
            if args.phase == "release" and status != "verified":
                errors.append(f"MAJOR evidence row {line}: status is not verified")
            if not source or Path(source).is_absolute() or ".." in Path(source).parts:
                errors.append(f"CRITICAL evidence row {line}: unsafe or missing source_path")
            elif not (root / source).is_file():
                errors.append(f"CRITICAL evidence row {line}: missing artifact {source}")

    literature_path = root / "05-evidence/literature-ledger.csv"
    if literature_path.is_file():
        rows = read_csv(literature_path, LIT_COLUMNS, errors)
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
        elif pdfs[0].stat().st_size > 20 * 1024 * 1024:
            errors.append("CRITICAL delivery PDF exceeds 20 MiB")
        audit_quality_report(root, pdfs[0] if len(pdfs) == 1 else None, errors)

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
