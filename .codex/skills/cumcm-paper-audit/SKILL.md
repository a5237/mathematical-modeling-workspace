---
name: cumcm-paper-audit
description: Independently audit CUMCM and similar mathematical modeling papers against project evidence, reproducibility, citations, anonymity, format, and delivery requirements. Use when Codex must review, score, red-team, compliance-check, or release-gate a mathematical modeling paper without inventing fixes or trusting unsupported author claims.
---

# CUMCM Paper Audit

Act as an independent reviewer. Do not silently repair the paper while auditing it.

All backticked repository paths in this skill are logical paths relative to the current workspace root. Before passing one to a file read, view, or edit tool that requires an absolute path, resolve it against the tool-recognized workspace root. Never pass `docs/...` or `.codex/...` unchanged to such a tool, and never guess `/docs/...` or `/.codex/...`; use the actual mounted or host workspace root reported by the environment. Relative paths remain appropriate for shell commands only when their working directory is explicitly the workspace root, and for project code that resolves paths reproducibly.

## Audit order

1. Read the problem statement, `docs/standards/workspace-governance.md`, `docs/standards/paper-writing.md`, `docs/standards/paper-quality-audit.md`, project manifest, problem checklist, `03-models/model-selection.md`, `00-admin/pre-writing-learning.md`, and paper.
2. Run `scripts/audit_cumcm_project.py <project> --phase release` and preserve its report in `07-review/`.
3. Re-run the documented computation entry point when feasible. Compare generated hashes, metrics, tables, and figures with cited evidence.
4. Confirm the model-selection record shows that matching algorithm-library resources were reviewed, applicable library algorithms were preferred, and every library deviation has a problem-specific reason and validation plan. Confirm the pre-writing record contains at least two actually reviewed same-type papers and the relevant algorithm learning; a `COMPLETE` label without substantive entries fails.
5. Trace every abstract number and conclusion through the body to a `verified` evidence row and an existing source artifact.
6. Check each subproblem for complete modeling logic and at least two applicable forms of supported analysis or equivalent evidence. Theoretical or otherwise inapplicable cases may use derivations, boundary checks, worked examples, or other substitutes, but the evidential strength must not be reduced.
7. Open every cited source; verify metadata and that it actually supports the adjacent claim. Confirm at least six references, actual in-text use of `数学模型（第五版）` and `数学建模算法与应用`, and at least four additional sources directly related to the problem. A real paper used for the wrong claim or added only to meet the count still fails. Treat citations listed in the algorithm library as unverified until independently opened.
8. Render the final delivery PDF page by page. Inspect page order, margins, overflow, figure/table captions, equation numbering, references, page count, and every figure's clarity and intuitiveness. Explicitly check for overlapping or clipped text, nodes, arrows, connectors, legends, labels, and ambiguous flowchart branches; source-file inspection is not sufficient.
9. Search paper, source, comments, filenames, metadata, and support materials for identity information.
10. Compare the appendix file list with the delivery archive and test runnable source code from a clean directory.
11. Classify findings using `references/audit-rubric.md`. Block release on any critical or major finding.
12. Write or update `07-review/paper-quality-audit.md` using `docs/standards/paper-quality-audit.md`. Give two independent verdicts: `paper-writing.md` compliance and national-award competitiveness. Do not infer that compliance alone implies award competitiveness.
13. If any paper, figure, table, or pagination changes after review, invalidate the prior PDF hash, re-render the affected output, and refresh both verdicts before release.

Never create missing experimental results, citations, checks, or sensitivity analyses as part of an audit. Report the absence and the exact evidence needed to clear it.
