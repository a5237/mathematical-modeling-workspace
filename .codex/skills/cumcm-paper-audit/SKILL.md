---
name: cumcm-paper-audit
description: Independently audit CUMCM and similar mathematical modeling papers against project evidence, reproducibility, citations, anonymity, format, and delivery requirements. Use when Codex must review, score, red-team, compliance-check, or release-gate a mathematical modeling paper without inventing fixes or trusting unsupported author claims.
---

# CUMCM Paper Audit

Act as an independent reviewer. Do not silently repair the paper while auditing it.

## Audit order

1. Read the problem statement, `数学建模工作区_Agent强制规范.md`, `数学建模论文写作_Agent强制规范.md`, project manifest, problem checklist, and paper.
2. Run `scripts/audit_cumcm_project.py <project> --phase release` and preserve its report in `07-review/`.
3. Re-run the documented computation entry point when feasible. Compare generated hashes, metrics, tables, and figures with cited evidence.
4. Trace every abstract number and conclusion through the body to a `verified` evidence row and an existing source artifact.
5. Check each subproblem for complete modeling logic and at least two applicable forms of supported analysis or equivalent evidence. Theoretical or otherwise inapplicable cases may use derivations, boundary checks, worked examples, or other substitutes, but the evidential strength must not be reduced.
6. Open every cited source; verify metadata and that it actually supports the adjacent claim. Confirm at least six references, actual in-text use of `数学模型（第五版）` and `数学建模算法与应用`, and at least four additional sources directly related to the problem. A real paper used for the wrong claim or added only to meet the count still fails.
7. Inspect the rendered PDF for page order, margins, overflow, illegible plots, figure/table captions, equation numbering, references, and page count.
8. Search paper, source, comments, filenames, metadata, and support materials for identity information.
9. Compare the appendix file list with the delivery archive and test runnable source code from a clean directory.
10. Classify findings using `references/audit-rubric.md`. Block release on any critical or major finding.

Never create missing experimental results, citations, checks, or sensitivity analyses as part of an audit. Report the absence and the exact evidence needed to clear it.
