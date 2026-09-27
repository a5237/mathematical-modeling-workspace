#!/usr/bin/env python3
"""Objective static preflight for mathematical modeling contest projects.

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
from pathlib import Path, PurePosixPath

import yaml

WORKSPACE_ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(WORKSPACE_ROOT / "tools"))

from control_contracts import (
    ContractError,
    contract_int,
    contract_optional_int,
    contract_optional_list,
    contract_optional_str,
    load_workspace_contracts,
    resolve_profile,
)


def project_identity(root: Path) -> tuple[str, str | None]:
    """Read the declared contest and, when present, the declared profile key."""

    path = root / "00-admin" / "project.yaml"
    try:
        config = yaml.safe_load(path.read_text(encoding="utf-8"))
    except OSError as exc:
        raise ContractError(f"cannot read project contest identity: {exc}") from exc
    except UnicodeDecodeError as exc:
        raise ContractError(f"{path.as_posix()} is not UTF-8: {exc}") from exc
    if not isinstance(config, dict):
        raise ContractError(f"project does not declare a contest in {path.relative_to(root).as_posix()}")
    contest = config.get("contest")
    if not isinstance(contest, str) or not contest:
        raise ContractError(f"project does not declare a contest in {path.relative_to(root).as_posix()}")
    declared = config.get("profile")
    return contest, declared if isinstance(declared, str) and declared else None


# Workspace records are authored in the workspace's own record language, so the
# unfilled markers are matched by word. The paper source is language-independent:
# an unfilled slot is the template macro itself, never a Chinese word.
RECORD_PLACEHOLDER = re.compile(r"TODO|TBD|FIXME|待填写|待定|待补|占位|XX+", re.IGNORECASE)
SOURCE_PLACEHOLDER = re.compile(r"\\TemplateField\{|TODO|TBD|FIXME")
AUDIT_FIELD = re.compile(r"^\s*-\s*([a-z0-9_]+):\s*`([^`]*)`\s*$", re.MULTILINE)
WORKFLOW_FIELD = re.compile(
    r"^\s*(?:[-*]\s*)?([a-z0-9_]+)\s*:\s*(.*?)\s*$", re.MULTILINE
)
FINAL_AUDIT_PATH = "07-review/final-audit.md"


def parse_unique_fields(
    pattern: re.Pattern[str],
    text: str,
    errors: list[str],
    label: str,
) -> dict[str, str]:
    """Parse ``key: value`` fields, rejecting repeats instead of last-wins.

    A repeat would let an appended compliant block silently overwrite a
    violating one, which is the whole point of the machine-readable summary.
    """

    fields: dict[str, str] = {}
    duplicates: set[str] = set()
    for key, raw_value in pattern.findall(text):
        if key in fields:
            duplicates.add(key)
        fields[key] = raw_value
    if duplicates:
        errors.append(f"MAJOR {label} repeats fields {sorted(duplicates)}")
    return fields


def workflow_metadata(text: str, errors: list[str]) -> dict[str, str]:
    fields = parse_unique_fields(WORKFLOW_FIELD, text, errors, "workflow record")
    for key, value in list(fields.items()):
        if len(value) >= 2 and value.startswith("`") and value.endswith("`"):
            fields[key] = value[1:-1].strip()
    return fields


def required_release_files(contracts) -> list[str]:
    """Core release artifacts plus the ones this contest's profile declares."""

    files = list(contracts.release_core_files)
    manifest = contract_optional_str(contracts, "delivery_manifest_path")
    if manifest:
        files.append(manifest)
    return files


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
    fields = workflow_metadata(text, errors)
    if fields.get(status_key) != expected_status:
        errors.append(f"MAJOR workflow gate {relative}: {status_key} must be {expected_status}")
    if RECORD_PLACEHOLDER.search(text):
        errors.append(f"MAJOR unresolved placeholder in {relative}")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def final_audit_path(root: Path) -> Path | None:
    current = root / FINAL_AUDIT_PATH
    return current if current.is_file() else None


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


def audit_declared_delivery_directories(root: Path, contracts, errors: list[str]) -> None:
    """Profile-declared delivery directories must exist and hold content.

    Git does not track empty directories, so a declared support-materials
    directory can disappear between commit and submission unchecked.
    """

    for relative in contract_optional_list(contracts, "extra_delivery_directories"):
        directory = root / relative
        if not directory.is_dir():
            errors.append(f"MAJOR missing profile-declared delivery directory: {relative}")
        elif not any(directory.rglob("*")):
            errors.append(f"MAJOR profile-declared delivery directory is empty: {relative}")


def audit_review_ledger(root: Path, contracts, fields: dict[str, str], errors: list[str]) -> None:
    """Cross-check the open finding counts against the review ledger.

    The summary's open counts and the ledger are authored by the same reviewer;
    a disagreement means one of them is stale, which is mechanically decidable.
    """

    path = root / "07-review" / "review-log.md"
    if not path.is_file():
        return
    columns = list(contracts.review_log_columns)
    if "severity" not in columns or "status" not in columns:
        return
    severity_at = columns.index("severity")
    status_at = columns.index("status")
    open_statuses = {token.upper() for token in contracts.review_open_statuses}
    open_rows: list[str] = []
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        if not line.lstrip().startswith("|"):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) != len(columns) or set("".join(cells)) <= set("-: "):
            continue
        if cells[status_at].upper() in open_statuses:
            open_rows.append(cells[severity_at].upper())
    for field in contracts.final_audit_zero_fields:
        if not field.startswith("open_"):
            continue
        reported = fields.get(field, "")
        if not reported.isdigit():
            continue
        severity = field[len("open_"):].upper()
        actual = sum(1 for token in open_rows if token == severity)
        if int(reported) != actual:
            errors.append(
                f"MAJOR review ledger records {actual} open {severity} findings "
                f"but final audit reports {reported}"
            )


PAGE_FIRST_LABEL = "page:counted-first"
PAGE_LAST_LABEL = "page:counted-last"
TEXT_FIRST_LABEL = "text:counted-first"
TEXT_LAST_LABEL = "text:counted-last"
LATEX_COMMENT = re.compile(r"(?<!\\)%[^\n]*")
NEWLABEL_PAGE = re.compile(r"\\newlabel\{([^{}]+)\}\{\{[^{}]*\}\{(\d+)\}")
FLOAT_ENVIRONMENTS = ("figure", "table")
NON_NARRATIVE_ENVIRONMENTS = (
    "figure",
    "table",
    "tabular",
    "tabularx",
    "array",
    "longtable",
    "lstlisting",
    "verbatim",
    "thebibliography",
    "equation",
    "align",
    "gather",
    "multline",
    "eqnarray",
)
LATEX_COMMAND = re.compile(r"\\[a-zA-Z]+\*?")
INLINE_MATH = re.compile(r"\$[^$]*\$")
HANZI = re.compile(r"[\u4e00-\u9fff]")
LATIN_WORD = re.compile(r"[A-Za-z]+")
NUMBER_TOKEN = re.compile(r"\d+(?:[.,]\d+)?")


def strip_latex_comments(text: str) -> str:
    return LATEX_COMMENT.sub("", text)


def remove_environments(text: str, names: tuple[str, ...]) -> str:
    for name in names:
        pattern = re.compile(
            r"\\begin\{" + re.escape(name) + r"\}.*?\\end\{" + re.escape(name) + r"\}",
            re.DOTALL,
        )
        text = pattern.sub("", text)
    return text


def counted_region(
    source: str,
    first_label: str,
    last_label: str,
    errors: list[str],
) -> str | None:
    """Return the paper source between two region labels."""

    start_at = source.find(f"\\label{{{first_label}}}")
    end_at = source.find(f"\\label{{{last_label}}}")
    if start_at < 0 or end_at < 0:
        missing = [
            name
            for name, at in ((first_label, start_at), (last_label, end_at))
            if at < 0
        ]
        errors.append(
            "MAJOR 06-paper/main.tex cannot delimit the counted region: missing "
            f"\\label{{{missing[0]}}}; compile the profile framework without removing its labels"
        )
        return None
    if end_at <= start_at:
        errors.append(
            f"MAJOR counted-region labels {first_label} and {last_label} are inverted in 06-paper/main.tex"
        )
        return None
    return source[start_at:end_at]


def count_narrative_length(region: str) -> int:
    """Apply the PW-LEN-001 counting rule: each Han char, Latin word and number counts 1."""

    prose = remove_environments(region, NON_NARRATIVE_ENVIRONMENTS)
    prose = INLINE_MATH.sub("", prose)
    prose = LATEX_COMMAND.sub(" ", prose)
    return (
        len(HANZI.findall(prose))
        + len(LATIN_WORD.findall(prose))
        + len(NUMBER_TOKEN.findall(prose))
    )


def count_floats(region: str) -> tuple[int, int]:
    figures = len(re.findall(r"\\begin\{figure\}", region))
    tables = len(re.findall(r"\\begin\{table\}", region))
    return figures, tables


def label_pages(root: Path, required: tuple[str, ...], errors: list[str]) -> dict[str, int]:
    aux = root / "06-paper" / "main.aux"
    if not aux.is_file():
        errors.append(
            "MAJOR cannot resolve the counted pages: 06-paper/main.aux is missing; "
            "run the final audit after compiling the paper"
        )
        return {}
    pages = {
        name: int(page)
        for name, page in NEWLABEL_PAGE.findall(aux.read_text(encoding="utf-8", errors="replace"))
    }
    for name in required:
        if name not in pages:
            errors.append(f"MAJOR 06-paper/main.aux does not resolve {name}")
    return pages


def pdf_page_count(path: Path, errors: list[str]) -> int | None:
    try:
        import pymupdf
    except ImportError:
        errors.append("MAJOR cannot read the delivery PDF: PyMuPDF is unavailable in this environment")
        return None
    try:
        with pymupdf.open(path) as document:
            return document.page_count
    except Exception as exc:
        errors.append(f"CRITICAL delivery PDF cannot be opened for page counting: {exc}")
        return None


def audit_derived_metrics(
    root: Path,
    contracts,
    delivery_pdf: Path | None,
    errors: list[str],
) -> None:
    """Derive length and visual counts from the paper source, aux and PDF.

    These budgets are the machine's own remit, so they are never taken from the
    reviewer's report: a self-reported count only proves a number was written.
    """

    source = root / "06-paper" / "main.tex"
    if not source.is_file():
        return
    clean = strip_latex_comments(source.read_text(encoding="utf-8", errors="replace"))

    page_region = counted_region(clean, PAGE_FIRST_LABEL, PAGE_LAST_LABEL, errors)
    if page_region is None:
        return

    figures, tables = count_floats(page_region)
    figure_minimum = contract_int(contracts, "body_figure_minimum")
    if figures < figure_minimum:
        errors.append(f"MAJOR counted figures {figures} is below body_figure_minimum {figure_minimum}")
    table_minimum = contract_int(contracts, "body_table_minimum")
    if tables < table_minimum:
        errors.append(f"MAJOR counted tables {tables} is below body_table_minimum {table_minimum}")

    word_minimum = contract_optional_int(contracts, "body_word_minimum") or 0
    if word_minimum:
        text_region = counted_region(clean, TEXT_FIRST_LABEL, TEXT_LAST_LABEL, errors)
        if text_region is not None:
            words = count_narrative_length(text_region)
            if words < word_minimum:
                errors.append(
                    f"MAJOR narrative length {words} is below body_word_minimum {word_minimum}"
                )

    page_minimum = contract_optional_int(contracts, "body_page_minimum") or 0
    page_maximum = contract_optional_int(contracts, "body_page_maximum") or 0
    if page_minimum and page_maximum and page_minimum > page_maximum:
        raise ContractError("body_page_minimum cannot exceed body_page_maximum")
    pages = label_pages(root, (PAGE_FIRST_LABEL, PAGE_LAST_LABEL), errors)
    if PAGE_FIRST_LABEL in pages and PAGE_LAST_LABEL in pages:
        first, last = pages[PAGE_FIRST_LABEL], pages[PAGE_LAST_LABEL]
        counted = last - first + 1
        if page_minimum and counted < page_minimum:
            errors.append(f"MAJOR counted pages {counted} is below body_page_minimum {page_minimum}")
        if page_maximum and counted > page_maximum:
            errors.append(f"MAJOR counted pages {counted} exceeds body_page_maximum {page_maximum}")
        if delivery_pdf is not None and delivery_pdf.is_file():
            total = pdf_page_count(delivery_pdf, errors)
            if total is not None and last > total:
                errors.append(
                    f"CRITICAL counted region ends on page {last} but the delivery PDF has {total} pages"
                )


def audit_final_report(
    root: Path,
    delivery_pdf: Path | None,
    contracts,
    phase: str,
    errors: list[str],
) -> None:
    path = final_audit_path(root)
    if path is None:
        errors.append(f"MAJOR missing final audit report: {FINAL_AUDIT_PATH}")
        return
    text = path.read_text(encoding="utf-8", errors="replace")
    fields = parse_unique_fields(AUDIT_FIELD, text, errors, "final audit summary")

    required = set(contracts.final_audit_fields)
    missing = sorted(required - fields.keys())
    if missing:
        errors.append(f"MAJOR {path}: missing final-audit fields {missing}")
        return
    if "## 机器可读摘要" not in text:
        errors.append(f"MAJOR {path.relative_to(root)} must contain the 机器可读摘要 section")
    sequence = [key for key, _ in AUDIT_FIELD.findall(text)]
    if sequence != list(contracts.final_audit_fields):
        errors.append("MAJOR final audit fields must appear in the contract order")
    if RECORD_PLACEHOLDER.search(text):
        errors.append(f"MAJOR unresolved placeholder in {path.relative_to(root)}")

    audit_derived_metrics(root, contracts, delivery_pdf, errors)
    audit_pdf_identity(root, delivery_pdf, fields, errors)
    audit_review_ledger(root, contracts, fields, errors)

    for key in contracts.final_audit_pass_fields:
        if fields[key] != contracts.final_audit_pass_status:
            errors.append(
                f"MAJOR final audit {key} is not {contracts.final_audit_pass_status}"
            )
    for key in contracts.final_audit_zero_fields:
        if fields[key] != contracts.final_audit_no_open_findings_value:
            errors.append(
                f"MAJOR final audit {key}: expected "
                f"{contracts.final_audit_no_open_findings_value!r}, found {fields[key]!r}"
            )
    if fields["release_decision"] != contracts.release_ready_status:
        errors.append(f"MAJOR final audit release_decision is {fields['release_decision']!r}")

    expected_phase = (
        contracts.release_candidate_phase_value
        if phase == "release-candidate"
        else contracts.final_phase_value
    )
    if fields["audit_phase"] != expected_phase:
        errors.append(f"MAJOR final audit audit_phase must be {expected_phase}")
    allowed_scope = set(
        contracts.release_candidate_review_scopes
        if phase == "release-candidate"
        else contracts.final_review_scopes
    )
    if fields["review_scope"] not in allowed_scope:
        errors.append(f"MAJOR final audit review_scope must be one of {sorted(allowed_scope)}")
    allowed_reproduction = set(
        contracts.release_candidate_reproduction_statuses
        if phase == "release-candidate"
        else contracts.final_reproduction_statuses
    )
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


def points_into_sandbox(value: str) -> bool:
    """Detect a project-relative reference to the reserved exploratory sandbox."""

    normalized = value.strip().replace("\\", "/")
    if not normalized:
        return False
    path = PurePosixPath(normalized)
    if path.parts and path.parts[0].casefold() == "sandbox":
        return True
    return re.search(r"(?:^|[\s\"'`=])sandbox/", normalized, re.IGNORECASE) is not None


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

    if not root.is_dir():
        parser.error(f"project does not exist: {root}")

    try:
        contest, declared_profile = project_identity(root)
        resolved_profile = resolve_profile(WORKSPACE_ROOT, contest) or ""
        contracts = load_workspace_contracts(WORKSPACE_ROOT, contest=contest)
    except ContractError as exc:
        print(f"CRITICAL authority contract: {exc}")
        return 2
    if declared_profile and declared_profile != resolved_profile:
        errors.append(
            f"CRITICAL project.yaml declares profile {declared_profile!r} but contest "
            f"{contest!r} resolves to {resolved_profile!r}"
        )

    if release_phase:
        for relative in required_release_files(contracts):
            if not (root / relative).is_file():
                errors.append(f"MAJOR missing release artifact: {relative}")
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
            generator = row.get("generator", "").strip()
            status = row.get("status", "").strip().lower()
            if status not in contracts.evidence_statuses:
                errors.append(f"MAJOR evidence row {line}: invalid status {status!r}")
            elif phase == "final" and status != contracts.evidence_verified_status:
                errors.append(
                    f"CRITICAL evidence row {line}: status {status!r} must be "
                    f"{contracts.evidence_verified_status!r} at the final phase"
                )
            if not source or Path(source).is_absolute() or ".." in Path(source).parts:
                errors.append(f"CRITICAL evidence row {line}: unsafe or missing source_path")
            elif points_into_sandbox(source):
                errors.append(
                    f"CRITICAL evidence row {line}: reserved sandbox/ artifact is non-authoritative"
                )
            elif not (root / source).is_file():
                errors.append(f"CRITICAL evidence row {line}: missing artifact {source}")
            if points_into_sandbox(generator):
                errors.append(
                    f"CRITICAL evidence row {line}: generator points into reserved sandbox/"
                )

    literature_path = root / "05-evidence/literature-ledger.csv"
    if literature_path.is_file():
        rows = read_csv(literature_path, set(contracts.literature_columns), errors)
        for line, row in enumerate(rows, 2):
            if release_phase and row.get("verified", "").strip().lower() not in {"yes", "true", "1"}:
                errors.append(f"MAJOR literature row {line}: source not verified")
            locator = row.get("doi_or_url", "").strip()
            if locator and not (locator.startswith("http://") or locator.startswith("https://") or locator.startswith("10.")):
                errors.append(f"MAJOR literature row {line}: invalid DOI/URL")

    if release_phase:
        for relative in required_release_files(contracts):
            path = root / relative
            if relative.endswith(".tex") or not path.is_file():
                continue
            if RECORD_PLACEHOLDER.search(path.read_text(encoding="utf-8", errors="replace")):
                errors.append(f"MAJOR unresolved placeholder in {relative}")
        paper_source = root / "06-paper/main.tex"
        if paper_source.is_file() and SOURCE_PLACEHOLDER.search(
            paper_source.read_text(encoding="utf-8", errors="replace")
        ):
            errors.append("MAJOR unfilled template slot remains in 06-paper/main.tex")

    pdfs = list((root / "08-delivery").glob("*.pdf")) if (root / "08-delivery").is_dir() else []
    if release_phase:
        audit_declared_delivery_directories(root, contracts, errors)
        if len(pdfs) != 1:
            errors.append(f"MAJOR delivery must contain exactly one PDF, found {len(pdfs)}")
        else:
            paper_limit = contract_int(contracts, "paper_maximum_bytes")
            if pdfs[0].stat().st_size > paper_limit:
                errors.append("CRITICAL delivery PDF exceeds the contest profile paper size limit")
            archive_limit = contract_optional_int(contracts, "archive_maximum_bytes")
            if archive_limit:
                for archive in sorted((root / "08-delivery").rglob("*")):
                    if not archive.is_file() or archive.suffix.lower() not in {".zip", ".rar"}:
                        continue
                    if archive.stat().st_size > archive_limit:
                        errors.append(
                            "CRITICAL delivery archive exceeds the contest profile archive size limit: "
                            + archive.relative_to(root).as_posix()
                        )
        audit_final_report(
            root,
            pdfs[0] if len(pdfs) == 1 else None,
            contracts,
            phase,
            errors,
        )
    else:
        missing_draft = [
            relative for relative in required_release_files(contracts) if not (root / relative).is_file()
        ]
        if missing_draft:
            warnings.append(
                "draft is incomplete, which is allowed; missing future release artifacts: "
                + ", ".join(missing_draft)
            )

    print(f"Audit root: {root}")
    print(f"Audit profile: {resolved_profile}")
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
