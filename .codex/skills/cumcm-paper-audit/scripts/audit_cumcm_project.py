#!/usr/bin/env python3
"""Objective static preflight for CUMCM projects.

Directory layout, ordinary naming, and reviewer judgment are intentionally out
of scope. The independent audit skill remains responsible for substantive
review and for recording a final verdict.
"""

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


# These are semantic handoff interfaces, not a directory-tree schema. Any other
# directories may be added, split, renamed or removed without this preflight
# caring about them.
RELEASE_CORE_FILES = [
    "00-admin/runbook.md",
    "00-admin/pre-writing-learning.md",
    "01-problem/problem-checklist.md",
    "03-models/model-selection.md",
    "05-evidence/evidence-index.csv",
    "05-evidence/literature-ledger.csv",
    "05-evidence/ai-tool-log.md",
    "06-paper/main.tex",
    "08-delivery/file-list.md",
]
PLACEHOLDER = re.compile(r"TODO|TBD|FIXME|待填写|待补|占位|XX+", re.IGNORECASE)
AUDIT_FIELD = re.compile(r"^\s*-\s*([a-z0-9_]+):\s*`([^`]*)`\s*$", re.MULTILINE)
WORKFLOW_FIELD = re.compile(
    r"^\s*(?:[-*]\s*)?([a-z0-9_]+)\s*:\s*(.*?)\s*$", re.MULTILINE
)
FINAL_AUDIT_PATH = "07-review/final-audit.md"
LEGACY_AUDIT_PATH = "07-review/paper-quality-audit.md"
FINAL_AUDIT_FIELDS = {
    "audit_date",
    "audit_phase",
    "review_scope",
    "final_pdf",
    "final_pdf_sha256",
    "body_word_count",
    "body_page_range",
    "body_page_count",
    "body_figure_count",
    "body_table_count",
    "body_length_and_visual_count_gate",
    "official_rules_gate",
    "evidence_gate",
    "clean_reproduction_gate",
    "anonymity_gate",
    "delivery_gate",
    "open_critical",
    "open_major",
    "release_decision",
}
def workflow_metadata(text: str) -> dict[str, str]:
    fields: dict[str, str] = {}
    for key, raw_value in WORKFLOW_FIELD.findall(text):
        value = raw_value.strip()
        if len(value) >= 2 and value.startswith("`") and value.endswith("`"):
            value = value[1:-1].strip()
        fields[key] = value
    return fields


def audit_workflow_gate(
    root: Path,
    relative: str,
    status_key: str,
    expected_status: str,
    errors: list[str],
) -> None:
    """Check only artifact existence and explicit stage completion.

    Substantive model-selection and learning quality remain reviewer duties. The
    static preflight intentionally does not bind intermediate content by hash or
    infer completeness from prose structure.
    """
    path = root / relative
    if not path.is_file():
        return
    text = path.read_text(encoding="utf-8", errors="replace")
    fields = workflow_metadata(text)
    if fields.get(status_key) != expected_status:
        errors.append(f"MAJOR workflow gate {relative}: {status_key} must be {expected_status}")
    if PLACEHOLDER.search(text):
        errors.append(f"MAJOR unresolved placeholder in {relative}")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def final_audit_path(root: Path) -> tuple[Path | None, bool]:
    current = root / FINAL_AUDIT_PATH
    if current.is_file():
        return current, False
    legacy = root / LEGACY_AUDIT_PATH
    if legacy.is_file():
        return legacy, True
    return None, False


def audit_count_fields(fields: dict[str, str], contracts, errors: list[str]) -> None:
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
        except (KeyError, ValueError):
            errors.append(f"MAJOR final audit field {key} must be an integer")
            continue
        parsed_counts[key] = value
        if value < minimum or (maximum is not None and value > maximum):
            expected_range = f">= {minimum}" if maximum is None else f"{minimum}..{maximum}"
            errors.append(f"MAJOR final audit field {key}: expected {expected_range}, found {value}")

    page_range = re.fullmatch(r"\s*(\d+)\s*[-–—]\s*(\d+)\s*", fields.get("body_page_range", ""))
    if page_range is None:
        errors.append("MAJOR final audit field body_page_range must use <start>-<end>")
    else:
        start_page, end_page = map(int, page_range.groups())
        if end_page < start_page:
            errors.append("MAJOR final audit body_page_range ends before it starts")
        elif "body_page_count" in parsed_counts and end_page - start_page + 1 != parsed_counts["body_page_count"]:
            errors.append("MAJOR final audit body_page_range does not match body_page_count")


def audit_pdf_identity(
    root: Path,
    delivery_pdf: Path | None,
    fields: dict[str, str],
    errors: list[str],
) -> None:
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", fields.get("audit_date", "")):
        errors.append("MAJOR final audit audit_date must use YYYY-MM-DD")
    if not re.fullmatch(r"[0-9a-fA-F]{64}", fields.get("final_pdf_sha256", "")):
        errors.append("MAJOR final audit final_pdf_sha256 must contain 64 hexadecimal characters")

    relative_pdf = Path(fields.get("final_pdf", ""))
    if not str(relative_pdf) or relative_pdf.is_absolute() or ".." in relative_pdf.parts:
        errors.append("CRITICAL final audit final_pdf is unsafe or missing")
        return
    reported_pdf = (root / relative_pdf).resolve()
    try:
        reported_pdf.relative_to(root)
    except ValueError:
        errors.append("CRITICAL final audit final_pdf escapes the project root")
        return
    if not reported_pdf.is_file():
        errors.append(f"CRITICAL final audit final_pdf does not exist: {relative_pdf}")
        return
    if delivery_pdf is not None and reported_pdf != delivery_pdf.resolve():
        errors.append("MAJOR final audit final_pdf is not the sole delivery PDF")
    if fields.get("final_pdf_sha256", "").lower() != sha256(reported_pdf):
        errors.append("CRITICAL final audit PDF hash does not match the reviewed delivery PDF")


def audit_final_report(
    root: Path,
    delivery_pdf: Path | None,
    contracts,
    phase: str,
    errors: list[str],
    warnings: list[str],
) -> None:
    path, legacy = final_audit_path(root)
    if path is None:
        errors.append(f"MAJOR missing final audit report: {FINAL_AUDIT_PATH}")
        return
    text = path.read_text(encoding="utf-8", errors="replace")
    fields = dict(AUDIT_FIELD.findall(text))

    common_fields = {
        "audit_date", "final_pdf", "final_pdf_sha256", "body_word_count",
        "body_page_range", "body_page_count", "body_figure_count", "body_table_count",
        "body_length_and_visual_count_gate", "open_critical", "open_major", "release_decision",
    }
    required = common_fields if legacy else FINAL_AUDIT_FIELDS
    missing = sorted(required - fields.keys())
    if missing:
        errors.append(f"MAJOR {path}: missing final-audit fields {missing}")
        return
    if PLACEHOLDER.search(text):
        errors.append(f"MAJOR unresolved placeholder in {path.relative_to(root)}")

    audit_count_fields(fields, contracts, errors)
    audit_pdf_identity(root, delivery_pdf, fields, errors)

    if fields["body_length_and_visual_count_gate"] != "PASS":
        errors.append("MAJOR retained body length/page/figure/table gate is not PASS")
    for key in ("open_critical", "open_major"):
        if fields[key] != "0":
            errors.append(f"MAJOR final audit {key}: expected '0', found {fields[key]!r}")
    if fields["release_decision"] != "READY":
        errors.append(f"MAJOR final audit release_decision is {fields['release_decision']!r}")

    if legacy:
        for key in (
            "paper_writing_compliance",
            "paper_figure_compliance",
            "full_pdf_render_review",
            "overlap_and_clipping",
        ):
            if fields.get(key) != "PASS":
                errors.append(f"MAJOR legacy final audit {key} is not PASS")
        warnings.append(
            f"legacy audit report accepted from {LEGACY_AUDIT_PATH}; use {FINAL_AUDIT_PATH} after the next substantive change"
        )
        return

    expected_phase = "RELEASE_CANDIDATE" if phase == "release-candidate" else "FINAL"
    if fields["audit_phase"] != expected_phase:
        errors.append(f"MAJOR final audit audit_phase must be {expected_phase}")
    allowed_scope = {"FULL"} if phase == "release-candidate" else {"FULL", "IMPACTED"}
    if fields["review_scope"] not in allowed_scope:
        errors.append(f"MAJOR final audit review_scope must be one of {sorted(allowed_scope)}")
    for key in ("official_rules_gate", "evidence_gate", "anonymity_gate", "delivery_gate"):
        if fields[key] != "PASS":
            errors.append(f"MAJOR final audit {key} is not PASS")
    allowed_reproduction = {"PASS"} if phase == "release-candidate" else {"PASS", "REUSED_UNCHANGED"}
    if fields["clean_reproduction_gate"] not in allowed_reproduction:
        errors.append(
            f"MAJOR final audit clean_reproduction_gate must be one of {sorted(allowed_reproduction)}"
        )


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
    parser.add_argument(
        "--phase",
        choices=("draft", "release-candidate", "final", "release"),
        default="draft",
        help="'release' is a compatibility alias for 'release-candidate'",
    )
    args = parser.parse_args()
    phase = "release-candidate" if args.phase == "release" else args.phase
    release_phase = phase != "draft"
    root = args.project.resolve()
    errors: list[str] = []
    warnings: list[str] = []

    try:
        contracts = load_workspace_contracts(WORKSPACE_ROOT)
    except ContractError as exc:
        print(f"CRITICAL authority contract: {exc}")
        return 2

    if not root.is_dir():
        parser.error(f"project does not exist: {root}")

    if release_phase:
        for relative in RELEASE_CORE_FILES:
            if not (root / relative).is_file():
                errors.append(f"MAJOR missing core release artifact: {relative}")
        audit_workflow_gate(
            root,
            "03-models/model-selection.md",
            "selection_status",
            contracts.selection_complete_status,
            errors,
        )
        audit_workflow_gate(
            root,
            "00-admin/pre-writing-learning.md",
            "learning_status",
            contracts.learning_complete_status,
            errors,
        )

    evidence_path = root / "05-evidence/evidence-index.csv"
    if evidence_path.is_file():
        rows = read_csv(evidence_path, set(contracts.claim_columns), errors)
        if release_phase and not rows:
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
            if release_phase and row.get("verified", "").strip().lower() not in {"yes", "true", "1"}:
                errors.append(f"MAJOR literature row {line}: source not verified")
            locator = row.get("doi_or_url", "").strip()
            if locator and not (locator.startswith("http://") or locator.startswith("https://") or locator.startswith("10.")):
                errors.append(f"MAJOR literature row {line}: invalid DOI/URL")

    for relative in ("01-problem/problem-checklist.md", "06-paper/main.tex", "08-delivery/file-list.md"):
        path = root / relative
        if path.is_file() and release_phase and PLACEHOLDER.search(path.read_text(encoding="utf-8", errors="replace")):
            errors.append(f"MAJOR unresolved placeholder in {relative}")

    pdfs = list((root / "08-delivery").glob("*.pdf")) if (root / "08-delivery").is_dir() else []
    if release_phase:
        if len(pdfs) != 1:
            errors.append(f"MAJOR delivery must contain exactly one PDF, found {len(pdfs)}")
        elif pdfs[0].stat().st_size > contracts.paper_maximum_bytes:
            errors.append("CRITICAL delivery PDF exceeds OFFICIAL-CUMCM-001 size limit")
        audit_final_report(
            root,
            pdfs[0] if len(pdfs) == 1 else None,
            contracts,
            phase,
            errors,
            warnings,
        )
    else:
        missing_draft = [relative for relative in RELEASE_CORE_FILES if not (root / relative).is_file()]
        if missing_draft:
            warnings.append(
                "draft is incomplete, which is allowed; missing future release artifacts: "
                + ", ".join(missing_draft)
            )

    print(f"Audit root: {root}")
    print(f"Audit phase: {phase}")
    for item in warnings:
        print(f"WARN - {item}")
    if errors:
        print("BLOCKED")
        for item in errors:
            print(f"- {item}")
        return 1
    print("PASS (objective static preflight; independent final review remains required)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
