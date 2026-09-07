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
    "docs/standards/evidence-contract.md",
    "docs/standards/paper-writing.md",
    "docs/standards/paper-quality-audit.md",
    "docs/guides/pre-writing-learning.md",
    "docs/standards/cumcm-current-rules.md",
)

CONTRACT_BLOCK = re.compile(
    r"^```toml[ \t]+machine-contract[ \t]*\r?\n(.*?)^```[ \t]*$",
    re.MULTILINE | re.DOTALL,
)

REQUIRED_KEYS = {
    "claim_columns",
    "literature_columns",
    "evidence_statuses",
    "body_word_minimum",
    "body_page_minimum",
    "body_page_maximum",
    "body_figure_minimum",
    "body_table_minimum",
    "learning_paper_minimum",
    "learning_complete_status",
    "selection_complete_status",
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

    for key in ("claim_columns", "literature_columns", "evidence_statuses"):
        raw = values[key]
        if not isinstance(raw, list) or not raw or not all(isinstance(item, str) and item for item in raw):
            raise ContractError(f"machine-contract key {key} must be a non-empty string array")
        values[key] = tuple(raw)

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
    return SimpleNamespace(**values)
