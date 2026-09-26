"""Load the small, explicit machine contracts embedded in authority documents.

Natural-language prose is intentionally not parsed. Only fenced blocks whose
info string is ``toml machine-contract`` participate in automation, so ordinary
documentation edits cannot break the initializer or static audit.

Contracts load in two segments. Core documents under ``docs/`` define the
contest-independent workspace contract. Contest profiles under
``config/contests/<profile>/`` provide contest-specific values (official
limits, disclosure formats). Callers with a project context pass ``contest``;
workspace-level callers omit it and receive the Core contract only.
"""

from __future__ import annotations

import re
import tomllib
from pathlib import Path
from types import SimpleNamespace

try:
    import yaml
except ImportError as exc:  # pragma: no cover - exercised only outside the workspace environment
    raise SystemExit(
        "PyYAML is required; run this tool with .venv-modeling/Scripts/python.exe"
    ) from exc


class ContractError(RuntimeError):
    pass


CORE_DOCUMENTS = (
    "docs/architecture/workspace-layout.md",
    "docs/standards/workspace-governance.md",
    "docs/standards/evidence-contract.md",
    "docs/standards/modeling-execution.md",
    "docs/standards/paper-writing.md",
    "docs/standards/paper-figures.md",
    "docs/standards/paper-quality-audit.md",
    "docs/guides/pre-writing-learning.md",
)

CONTEST_PROFILE_ROOT = Path("config/contests")
PROFILE_CONFIG_NAME = "profile.yaml"

CONTRACT_BLOCK = re.compile(
    r"^```toml[ \t]+machine-contract[ \t]*\r?\n(.*?)^```[ \t]*$",
    re.MULTILINE | re.DOTALL,
)

CORE_REQUIRED_KEYS = {
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
}

STRING_ARRAY_KEYS = (
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

NONEMPTY_STRING_KEYS = (
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
)

POSITIVE_INT_KEYS = (
    "body_word_minimum",
    "body_page_minimum",
    "body_page_maximum",
    "body_figure_minimum",
    "body_table_minimum",
    "learning_paper_minimum",
    "paper_maximum_bytes",
)


def _document_blocks(root: Path, relative: str) -> dict[str, object]:
    path = root / relative
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as exc:
        raise ContractError(f"cannot read authority file {relative}: {exc}") from exc

    blocks = CONTRACT_BLOCK.findall(text)
    if not blocks:
        raise ContractError(f"missing explicit machine-contract block in {relative}")
    values: dict[str, object] = {}
    for block in blocks:
        try:
            parsed = tomllib.loads(block)
        except tomllib.TOMLDecodeError as exc:
            raise ContractError(f"invalid machine contract in {relative}: {exc}") from exc
        duplicates = sorted(values.keys() & parsed.keys())
        if duplicates:
            raise ContractError(f"duplicate machine-contract keys {duplicates} in {relative}")
        values.update(parsed)
    return values


def _load_profile_config(root: Path, profile: str) -> dict[str, object]:
    path = root / CONTEST_PROFILE_ROOT / profile / PROFILE_CONFIG_NAME
    try:
        config = yaml.safe_load(path.read_text(encoding="utf-8"))
    except OSError as exc:
        raise ContractError(f"cannot read contest profile config {profile}: {exc}") from exc
    if not isinstance(config, dict):
        raise ContractError(f"invalid contest profile config for {profile}")
    contests = config.get("contests")
    contract_keys = config.get("contract_keys")
    paper_framework = config.get("paper_framework")
    if (
        not isinstance(contests, list)
        or not contests
        or not all(isinstance(item, str) and item for item in contests)
    ):
        raise ContractError(f"contest profile {profile} must declare a non-empty 'contests' list")
    if (
        not isinstance(contract_keys, list)
        or not all(isinstance(item, str) and item for item in contract_keys)
    ):
        raise ContractError(f"contest profile {profile} must declare a 'contract_keys' string list")
    if not isinstance(paper_framework, str) or not paper_framework:
        raise ContractError(f"contest profile {profile} must declare a 'paper_framework' path")
    return config


def resolve_profile(root: Path, contest: str) -> str | None:
    """Map a contest identifier to its profile directory name."""

    profile_root = root / CONTEST_PROFILE_ROOT
    if not profile_root.is_dir():
        return None
    profiles = sorted(entry.name for entry in profile_root.iterdir() if entry.is_dir())
    if contest in profiles:
        return contest
    for profile in profiles:
        config = _load_profile_config(root, profile)
        if contest in config["contests"]:
            return profile
    return None


def available_profiles(root: Path) -> list[str]:
    profile_root = root / CONTEST_PROFILE_ROOT
    if not profile_root.is_dir():
        return []
    return sorted(entry.name for entry in profile_root.iterdir() if entry.is_dir())


def available_contests(root: Path) -> list[str]:
    contests: list[str] = []
    for profile in available_profiles(root):
        config = _load_profile_config(root, profile)
        contests.extend(config["contests"])
    return sorted(contests)


def _profile_documents(root: Path, profile: str) -> list[str]:
    profile_dir = root / CONTEST_PROFILE_ROOT / profile
    return sorted(
        path.relative_to(root).as_posix()
        for path in profile_dir.rglob("*.md")
        if path.is_file()
    )


def _validate(values: dict[str, object]) -> None:
    for key in STRING_ARRAY_KEYS:
        if key not in values:
            continue
        raw = values[key]
        if not isinstance(raw, list) or not raw or not all(isinstance(item, str) and item for item in raw):
            raise ContractError(f"machine-contract key {key} must be a non-empty string array")
        values[key] = tuple(raw)

    for key in NONEMPTY_STRING_KEYS:
        if key not in values:
            continue
        if not isinstance(values[key], str) or not values[key]:
            raise ContractError(f"machine-contract key {key} must be a non-empty string")

    for key in POSITIVE_INT_KEYS:
        if key not in values:
            continue
        if not isinstance(values[key], int) or values[key] <= 0:
            raise ContractError(f"machine-contract key {key} must be a positive integer")

    if "body_page_minimum" in values and "body_page_maximum" in values:
        if values["body_page_minimum"] > values["body_page_maximum"]:
            raise ContractError("body_page_minimum cannot exceed body_page_maximum")

    if "artifact_impact_defaults" in values:
        impact_defaults = values["artifact_impact_defaults"]
        if not isinstance(impact_defaults, dict) or not impact_defaults:
            raise ContractError("machine-contract key artifact_impact_defaults must be a non-empty table")
        known_categories = set(values.get("artifact_path_categories", ())) | set(
            values.get("artifact_semantic_categories", ())
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

    if "artifact_index_categories" in values:
        index_categories = values["artifact_index_categories"]
        if (
            not isinstance(index_categories, dict)
            or not index_categories
            or any(name not in values.get("artifact_index_names", ()) for name in index_categories)
            or any(
                category not in (set(values.get("artifact_path_categories", ())) | set(values.get("artifact_semantic_categories", ())))
                for category in index_categories.values()
            )
        ):
            raise ContractError("invalid artifact_index_categories machine contract")


def load_workspace_contracts(root: Path, contest: str | None = None):
    """Return validated objective values from explicit TOML contract blocks.

    Without ``contest``, only the Core contract is loaded and its closed key
    set is enforced. With ``contest``, the contest profile is resolved and its
    contract keys are merged on top of Core.
    """

    values: dict[str, object] = {}
    for relative in CORE_DOCUMENTS:
        values.update(_document_blocks(root, relative))

    missing = sorted(CORE_REQUIRED_KEYS - values.keys())
    extras = sorted(values.keys() - CORE_REQUIRED_KEYS)
    if missing or extras:
        details = []
        if missing:
            details.append(f"missing keys {missing}")
        if extras:
            details.append(f"unknown keys {extras}")
        raise ContractError("invalid Core machine contract: " + "; ".join(details))

    if contest is not None:
        profile = resolve_profile(root, contest)
        if profile is None:
            known = ", ".join(available_contests(root)) or "none"
            raise ContractError(f"unknown contest '{contest}'; available contests: {known}")
        config = _load_profile_config(root, profile)
        expected = set(config["contract_keys"])
        profile_values: dict[str, object] = {}
        for relative in _profile_documents(root, profile):
            for key, value in _document_blocks(root, relative).items():
                if key in profile_values:
                    raise ContractError(f"duplicate machine-contract key {key} in contest profile {profile}")
                if key in CORE_REQUIRED_KEYS:
                    raise ContractError(f"contest profile {profile} cannot redefine Core key {key}")
                profile_values[key] = value
        if set(profile_values) != expected:
            raise ContractError(
                f"contest profile {profile} contract keys {sorted(profile_values)} "
                f"do not match profile.yaml contract_keys {sorted(expected)}"
            )
        values.update(profile_values)

    _validate(values)
    return SimpleNamespace(**values)
