"""Read machine-enforced values from authority Markdown."""

import re
from pathlib import Path
from types import SimpleNamespace


class ContractError(RuntimeError):
    pass


DOCUMENTS = (
    "docs/standards/evidence-contract.md",
    "docs/standards/paper-writing.md",
    "docs/standards/paper-quality-audit.md",
    "docs/guides/pre-writing-learning.md",
    "docs/standards/cumcm-current-rules.md",
)


def load_workspace_contracts(root: Path):
    def read(relative: str) -> str:
        try:
            return (root / relative).read_text(encoding="utf-8")
        except OSError as exc:
            raise ContractError(f"cannot read authority file {relative}: {exc}") from exc

    def match(pattern: str, text: str, label: str, flags: int = 0):
        found = re.search(pattern, text, flags)
        if found is None:
            raise ContractError(f"cannot parse {label} from authority Markdown")
        return found

    def ticks(pattern: str, text: str, label: str) -> tuple[str, ...]:
        return tuple(re.findall(r"`([^`]+)`", match(pattern, text, label).group(1)))

    evidence, paper, quality, learning, official = map(read, DOCUMENTS)
    claims = match(r"`05-evidence/evidence-index\.csv`[^\n]*\n\n([\s\S]*?)\n\n发布前", evidence, "evidence columns").group(1)
    report = match(r"## 6\.[\s\S]*?PQA-REPORT-001[\s\S]*?```markdown\s*\n([\s\S]*?)\n```", quality, "quality report template").group(1).strip() + "\n"
    options = {
        key: tuple(re.findall(r"`([^`]+)`", description))
        for key, description in re.findall(r"^- ([a-z0-9_]+):\s*(.*)$", report, re.MULTILINE)
    }
    if not options:
        raise ContractError("quality report template contains no fields")
    figures = match(r"正文必须至少包含\s*\*\*(\d+) 个图\*\*和\s*\*\*(\d+) 个表\*\*", quality, "minimum visual counts")
    pages = match(r"正文必须为\s*\*\*(\d+)\s*[—-]\s*(\d+) 页\*\*", quality, "body page range")

    return SimpleNamespace(
        claim_columns=tuple(re.findall(r"^- `([a-z0-9_]+)`：", claims, re.MULTILINE)),
        literature_columns=tuple(match(r"`05-evidence/literature-ledger\.csv`[^\n]*\n\n`([^`]+)`", evidence, "literature columns").group(1).split(",")),
        evidence_statuses=ticks(r"`status`：([^\n]+)", claims, "evidence statuses"),
        body_word_minimum=int(match(r"PW-LEN-001[\s\S]{0,300}?\*\*([\d,]+) 字\*\*", paper, "minimum body words").group(1).replace(",", "")),
        body_page_minimum=int(pages.group(1)),
        body_page_maximum=int(pages.group(2)),
        body_figure_minimum=int(figures.group(1)),
        body_table_minimum=int(figures.group(2)),
        quality_report_template=report,
        quality_field_options=options,
        quality_finding_fields=ticks(r"每[项条]发现必须包含：\s*\n\n([^\n]+)", quality, "quality finding fields"),
        learning_paper_minimum=int(match(r"至少\s*(\d+)\s*篇", learning, "learning paper minimum").group(1)),
        learning_complete_status=match(r"`learning_status`[^\n]*?`([^`]+)`", learning, "learning completion status").group(1),
        selection_complete_status=match(r"`selection_status`[^\n]*?`([^`]+)`", learning, "selection completion status").group(1),
        paper_maximum_bytes=int(float(match(r"电子论文[^\n]*?不超过\s*([\d.]+)\s*MB", official, "maximum paper size", re.IGNORECASE).group(1)) * 1_000_000),
    )
