---
name: cumcm-paper-audit
description: Independently audit CUMCM and similar mathematical modeling papers against project evidence, reproducibility, citations, anonymity, format, and delivery requirements. Use when Codex must review, score, red-team, compliance-check, or release-gate a mathematical modeling paper without inventing fixes or trusting unsupported author claims.
---

# CUMCM Paper Audit

Act as an independent reviewer. Do not silently repair the paper while auditing it.

Repository paths in this skill are logical paths relative to the current workspace root and follow the resolution convention in `AGENTS.md`. Read `docs/README.md` for the authority matrix. This skill defines audit order only; thresholds, counts, schemas, official rules and paper requirements remain in their authority documents.

## Audit order

1. Read the problem statement, authority documents required by `docs/README.md`, project manifest, problem checklist, model-selection record, learning record and paper.
2. Run `scripts/audit_cumcm_project.py <project> --phase release` and preserve its report in `07-review/`.
3. Re-run the documented computation entry point when feasible. Compare generated hashes, metrics, tables, and figures with cited evidence.
4. Verify `WG-MODEL-001` and `PWL-GATE-001` from substantive record contents; labels without evidence fail.
5. Trace paper claims and citations under `WG-EVID-001`, opening cited sources and confirming support for adjacent claims.
6. Check each subproblem against `PW-VAL-001` and the complete modeling requirements in `docs/standards/paper-writing.md`.
7. Check every paper figure against `docs/standards/paper-figures.md` and determine `PW-FIG-001` from the final rendered PDF.
8. Check the reference list and in-text use against `PW-CITE-001` without inventing or padding sources.
9. Render the final delivery PDF page by page. Inspect page order, margins, overflow, table captions, equation numbering, references and page count; do not substitute source-file inspection for final-page review.
10. Search paper, source, comments, filenames, metadata and support materials for identity information, and enforce `OFFICIAL-CUMCM-001`.
11. Compare the appendix file list with the delivery archive and test runnable source code from a clean directory.
12. Classify findings using `references/audit-rubric.md`. Block release on any critical or major finding.
13. Write or update `07-review/paper-quality-audit.md` under `PQA-REPORT-001` and determine release under `PQA-RELEASE-001`.
14. If any paper, figure, table, or pagination changes after review, invalidate the prior PDF hash, re-render the affected output, and refresh both verdicts before release.

Never create missing experimental results, citations, checks, or sensitivity analyses as part of an audit. Report the absence and the exact evidence needed to clear it.
