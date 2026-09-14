"""Load the small, explicit machine contracts embedded in authority documents.

Natural-language prose is intentionally not parsed. Only fenced blocks whose
info string is ``toml machine-contract`` participate in automation, so ordinary
documentation edits cannot break the initializer or static audit.
"""

from __future__ import annotations

import re
from pathlib import Path
from types import SimpleNamespace

try:
    import tomllib
except ModuleNotFoundError:  # Python 3.10 compatibility
    import tomli as tomllib


class ContractError(RuntimeError):
    pass


DOCUMENTS = (
    "docs/architecture/workspace-layout.md",
    "docs/standards/workspace-governance.md",
    "docs/standards/evidence-contract.md",
    "docs/standards/modeling-execution.md",
    "docs/standards/paper-writing.md",
    "docs/standards/paper-figures.md",
    "docs/standards/paper-quality-audit.md",
    "docs/guides/pre-writing-learning.md",
    "docs/standards/cumcm-current-rules.md",
)

CONTRACT_BLOCK = re.compile(
    r"^```toml[ \t]+machine-contract[ \t]*\r?\n(.*?)^```[ \t]*$",
    re.MULTILINE | re.DOTALL,
)

REQUIRED_KEYS = {
    "recommended_project_directories",
    "artifact_path_categories",
    "artifact_semantic_categories",
    "artifact_index_names",
    "artifact_question_evidence_fields",
    "artifact_index_categories",
    "artifact_impact_defaults",
    "problem_attachment_columns",
    "problem_question_columns",
    "problem_risk_columns",
    "ai_log_columns",
    "claim_columns",
    "literature_columns",
    "evidence_statuses",
    "selection_complete_status",
    "selection_initial_status",
    "model_selection_columns",
    "body_word_minimum",
    "figure_registry_columns",
    "figure_risk_columns",
    "figure_final_pdf_statuses",
    "figure_initial_status",
    "body_page_minimum",
    "body_page_maximum",
    "body_figure_minimum",
    "body_table_minimum",
    "release_core_files",
    "review_log_columns",
    "final_audit_fields",
    "final_audit_pass_fields",
    "final_audit_zero_fields",
    "release_candidate_phase_value",
    "final_phase_value",
    "release_candidate_review_scopes",
    "final_review_scopes",
    "release_candidate_reproduction_statuses",
    "final_reproduction_statuses",
    "final_audit_pass_status",
    "final_audit_no_open_findings_value",
    "release_ready_status",
    "learning_paper_minimum",
    "learning_complete_status",
    "learning_initial_status",
    "learning_sample_columns",
    "learning_algorithm_columns",
    "paper_maximum_bytes",
}


def load_workspace_contracts(root: Path):
    """Return validated objective values from explicit TOML contract blocks."""

    values: dict[str, object] = {}
    for relative in DOCUMENTS:
        path = root / relative
        try:
            text = path.read_text(encoding="utf-8")
        except OSError as exc:
            raise ContractError(f"cannot read authority file {relative}: {exc}") from exc

        blocks = CONTRACT_BLOCK.findall(text)
        if not blocks:
            raise ContractError(f"missing explicit machine-contract block in {relative}")
        for block in blocks:
            try:
                parsed = tomllib.loads(block)
            except tomllib.TOMLDecodeError as exc:
                raise ContractError(f"invalid machine contract in {relative}: {exc}") from exc
            duplicates = sorted(values.keys() & parsed.keys())
            if duplicates:
                raise ContractError(f"duplicate machine-contract keys {duplicates} in {relative}")
            values.update(parsed)

    missing = sorted(REQUIRED_KEYS - values.keys())
    extras = sorted(values.keys() - REQUIRED_KEYS)
    if missing or extras:
        details = []
        if missing:
            details.append(f"missing keys {missing}")
        if extras:
            details.append(f"unknown keys {extras}")
        raise ContractError("invalid machine contract: " + "; ".join(details))

    string_arrays = (
        "recommended_project_directories",
        "artifact_path_categories",
        "artifact_semantic_categories",
        "artifact_index_names",
        "artifact_question_evidence_fields",
        "problem_attachment_columns",
        "problem_question_columns",
        "problem_risk_columns",
        "ai_log_columns",
        "claim_columns",
        "literature_columns",
        "evidence_statuses",
        "model_selection_columns",
        "figure_registry_columns",
        "figure_risk_columns",
        "figure_final_pdf_statuses",
        "release_core_files",
        "review_log_columns",
        "final_audit_fields",
        "final_audit_pass_fields",
        "final_audit_zero_fields",
        "release_candidate_review_scopes",
        "final_review_scopes",
        "release_candidate_reproduction_statuses",
        "final_reproduction_statuses",
        "learning_sample_columns",
        "learning_algorithm_columns",
    )
    for key in string_arrays:
        raw = values[key]
        if not isinstance(raw, list) or not raw or not all(isinstance(item, str) and item for item in raw):
            raise ContractError(f"machine-contract key {key} must be a non-empty string array")
        values[key] = tuple(raw)

    for key in (
        "selection_complete_status",
        "selection_initial_status",
        "figure_initial_status",
        "release_candidate_phase_value",
        "final_phase_value",
        "final_audit_pass_status",
        "final_audit_no_open_findings_value",
        "release_ready_status",
        "learning_complete_status",
        "learning_initial_status",
    ):
        if not isinstance(values[key], str) or not values[key]:
            raise ContractError(f"machine-contract key {key} must be a non-empty string")

    for key in (
        "body_word_minimum",
        "body_page_minimum",
        "body_page_maximum",
        "body_figure_minimum",
        "body_table_minimum",
        "learning_paper_minimum",
        "paper_maximum_bytes",
    ):
        if not isinstance(values[key], int) or values[key] <= 0:
            raise ContractError(f"machine-contract key {key} must be a positive integer")

    if values["body_page_minimum"] > values["body_page_maximum"]:
        raise ContractError("body_page_minimum cannot exceed body_page_maximum")

    impact_defaults = values["artifact_impact_defaults"]
    if not isinstance(impact_defaults, dict) or not impact_defaults:
        raise ContractError("machine-contract key artifact_impact_defaults must be a non-empty table")
    known_categories = set(values["artifact_path_categories"]) | set(
        values["artifact_semantic_categories"]
    )
    for target, spec in impact_defaults.items():
        if target not in known_categories or not isinstance(spec, dict):
            raise ContractError(f"invalid artifact impact target: {target}")
        dependencies = spec.get("depends_on")
        effect = spec.get("effect")
        if (
            not isinstance(dependencies, list)
            or not dependencies
            or any(item not in known_categories for item in dependencies)
            or effect not in {"STALE", "RECHECK"}
        ):
            raise ContractError(f"invalid artifact impact rule: {target}")

    index_categories = values["artifact_index_categories"]
    if (
        not isinstance(index_categories, dict)
        or not index_categories
        or any(name not in values["artifact_index_names"] for name in index_categories)
        or any(category not in known_categories for category in index_categories.values())
    ):
        raise ContractError("invalid artifact_index_categories machine contract")
    return SimpleNamespace(**values)
