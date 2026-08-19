---
name: cumcm-paper-production
description: Build and operate an evidence-driven production system for CUMCM and similar mathematical modeling contest papers. Use when Codex must initialize a contest project, analyze a problem, select models, implement and run computations, generate traceable tables or figures, write or revise a paper from real outputs, maintain citations and AI-use records, or prepare reproducible submission materials.
---

# CUMCM Paper Production

All backticked repository paths in this skill are logical paths relative to the current workspace root. Before passing one to a file read, view, or edit tool that requires an absolute path, resolve it against the tool-recognized workspace root. Never pass `docs/...` or `.codex/...` unchanged to such a tool, and never guess `/docs/...` or `/.codex/...`; use the actual mounted or host workspace root reported by the environment. Relative paths remain appropriate for shell commands only when their working directory is explicitly the workspace root, and for project code that resolves paths reproducibly.

Read the workspace `docs/standards/workspace-governance.md` first and treat it as the operational baseline. Before model construction or code implementation, read `resources/algorithm-library/index.md` and then only the algorithm documents matching the current subproblems. When the task involves paper content, formatting, or appendices, also read `docs/standards/paper-writing.md` and `docs/guides/pre-writing-learning.md` and treat them as the writing baseline and startup gate.

Keep the boundary strict: environments, dependency versions, run entry points, file paths, logs, evidence ledgers, and full reproduction instructions belong to the workspace record. Put them in the paper only when they directly affect the model, result, or an official appendix requirement.

## Execute the gated workflow

1. Inventory the statement, attachments, data schema, units, missing values, constraints, and every requested output. Record them in `01-problem/problem-checklist.md`.
2. For each subproblem, state inputs, outputs, evaluation metrics, dependencies, and at least one baseline. Use the algorithm-library index to locate matching documents, compare candidates, and record the decision in `03-models/model-selection.md`. Prefer an applicable library algorithm; use a method outside the library only when coverage or applicability is insufficient or the alternative has a problem-specific, verifiable advantage, and record that deviation. Limit each subproblem to at most two independent main model systems; baselines and validation comparators do not count as additional main systems.
3. Define variables, parameters, objective or governing relations, constraints, assumptions, validation strategy, and solver strategy before coding. Mark `selection_status` as `COMPLETE` only after the suitability and dependency checks are real.
4. Adapt library code examples to the project rather than copying them as finished code. Run code in the project environment, fix seeds, use relative paths, preserve raw data, save parameters and logs, and emit stable machine-readable outputs.
5. Validate dimensions, bounds, constraints, representative cases, and a baseline or other suitable comparator when applicable. For each subproblem, complete at least two applicable forms of result analysis, error analysis, model validation, sensitivity/robustness analysis, or equivalent evidence. Theoretical or otherwise inapplicable cases must use derivations, boundary checks, worked examples, or other substitutes without reducing evidential strength.
6. Register every material numerical or factual claim in `05-evidence/evidence-index.csv` before writing it into the paper. Never infer a specific value from an unsaved console display.
7. Register every cited source in `05-evidence/literature-ledger.csv`; require an actual retrieval URL or DOI and verification date. The paper should contain at least six references, must include and actually cite `数学模型（第五版）` and `数学建模算法与应用`, and must include at least four additional sources directly related to the problem, model, algorithm, parameters, or validation. Treat bibliography entries in the algorithm library as leads only; do not cite them until independently opened and verified.
8. Before drafting any paper section, execute `docs/guides/pre-writing-learning.md`: read at least two same-type high-quality papers, review the selected algorithm documents, record structural lessons without copying, and set `00-admin/pre-writing-learning.md` to `COMPLETE`.
9. Write sections from verified evidence. Keep abstract, body, tables, figures, appendix, and code outputs numerically identical.
10. Record AI assistance continuously in `05-evidence/ai-tool-log.md`, including purpose, important prompts and responses, adoption, and human changes.
11. Invoke the independent audit skill and clear every blocker before release.

## Use bundled resources

- Run `scripts/init_cumcm_project.py` to create a normalized project tree.
- Read `resources/algorithm-library/index.md` before model selection and then load only the matching algorithm document. The library is a preferred candidate and implementation reference, not a substitute for problem-specific reasoning, testing, or source verification.
- Read `docs/guides/pre-writing-learning.md` immediately before paper drafting and complete the generated project learning record.
- Read `references/evidence-contract.md` before producing concrete results or citations.
- Read `references/current-cumcm-rules.md` for the verified 2026 format and AI disclosure baseline; browse the official site again immediately before a real submission.
- Follow the workspace `docs/standards/naming.md` for all stable artifact names.

## Stop conditions

Do not begin formal model implementation before `03-models/model-selection.md` records the resource-library review and reaches `COMPLETE`. Do not begin paper drafting before `00-admin/pre-writing-learning.md` reaches `COMPLETE`. Do not write concrete numerical results if code has not run successfully or the output artifact is missing. Do not claim validation, robustness, accuracy, optimality, or sensitivity without recorded tests. Mark missing inputs and unresolved claims explicitly and continue only with symbolic structure where useful.
