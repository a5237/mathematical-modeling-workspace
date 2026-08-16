#!/usr/bin/env python3
"""Static release gate for normalized CUMCM projects."""

from __future__ import annotations

import argparse
import csv
import re
import sys
from pathlib import Path


REQUIRED_DIRS = ["00-admin", "01-problem", "02-data/raw", "03-models", "04-results", "05-evidence", "06-paper", "07-review", "08-delivery"]
REQUIRED_FILES = ["00-admin/project.yaml", "01-problem/problem-checklist.md", "05-evidence/evidence-index.csv", "05-evidence/literature-ledger.csv", "05-evidence/ai-tool-log.md", "06-paper/main.tex", "07-review/review-log.md", "08-delivery/file-list.md"]
PLACEHOLDER = re.compile(r"TODO|TBD|FIXME|待填写|待补|占位|XX+", re.IGNORECASE)
CLAIM_COLUMNS = {"claim_id", "question_id", "claim", "evidence_type", "source_path", "generator", "generated_at", "status"}
LIT_COLUMNS = {"citation_key", "title", "authors", "year", "doi_or_url", "retrieved_at", "used_in", "verified"}


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

    print(f"Audit root: {root}")
    if errors:
        print("BLOCKED")
        for item in errors:
            print(f"- {item}")
        return 1
    print("PASS (static checks only; manual and reproducibility review still required)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
