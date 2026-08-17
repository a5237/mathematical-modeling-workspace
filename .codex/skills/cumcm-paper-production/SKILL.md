---
name: cumcm-paper-production
description: Build and operate an evidence-driven production system for CUMCM and similar mathematical modeling contest papers. Use when Codex must initialize a contest project, analyze a problem, select models, implement and run computations, generate traceable tables or figures, write or revise a paper from real outputs, maintain citations and AI-use records, or prepare reproducible submission materials.
---

# CUMCM Paper Production

Read the workspace `docs/standards/workspace-governance.md` first and treat it as the operational baseline. When the task involves paper content, formatting, or appendices, also read `docs/standards/paper-writing.md` and treat it as the paper-writing baseline.

Keep the boundary strict: environments, dependency versions, run entry points, file paths, logs, evidence ledgers, and full reproduction instructions belong to the workspace record. Put them in the paper only when they directly affect the model, result, or an official appendix requirement.

## Execute the gated workflow

1. Inventory the statement, attachments, data schema, units, missing values, constraints, and every requested output. Record them in `01-problem/problem-checklist.md`.
2. For each subproblem, state inputs, outputs, evaluation metrics, dependencies, and at least one baseline. Compare candidate models before choosing one.
3. Define variables, parameters, objective or governing relations, constraints, assumptions, and solver strategy before coding.
4. Run code in the project environment. Fix seeds, use relative paths, preserve raw data, save parameters and logs, and emit stable machine-readable outputs.
5. Validate dimensions, bounds, constraints, representative cases, and a baseline or other suitable comparator when applicable. For each subproblem, complete at least two applicable forms of result analysis, error analysis, model validation, sensitivity/robustness analysis, or equivalent evidence. Theoretical or otherwise inapplicable cases must use derivations, boundary checks, worked examples, or other substitutes without reducing evidential strength.
6. Register every material numerical or factual claim in `05-evidence/evidence-index.csv` before writing it into the paper. Never infer a specific value from an unsaved console display.
7. Register every cited source in `05-evidence/literature-ledger.csv`; require an actual retrieval URL or DOI and verification date. The paper should contain at least six references, must include and actually cite `数学模型（第五版）` and `数学建模算法与应用`, and must include at least four additional sources directly related to the problem, model, algorithm, parameters, or validation. Do not cite a search-result snippet or add irrelevant filler.
8. Write sections from verified evidence. Keep abstract, body, tables, figures, appendix, and code outputs numerically identical.
9. Record AI assistance continuously in `05-evidence/ai-tool-log.md`, including purpose, important prompts and responses, adoption, and human changes.
10. Invoke the independent audit skill and clear every blocker before release.

## Use bundled resources

- Run `scripts/init_cumcm_project.py` to create a normalized project tree.
- Read `references/evidence-contract.md` before producing concrete results or citations.
- Read `references/current-cumcm-rules.md` for the verified 2026 format and AI disclosure baseline; browse the official site again immediately before a real submission.
- Follow the workspace `docs/standards/naming.md` for all stable artifact names.

## Stop conditions

Do not write concrete numerical results if code has not run successfully or the output artifact is missing. Do not claim validation, robustness, accuracy, optimality, or sensitivity without recorded tests. Mark missing inputs and unresolved claims explicitly and continue only with symbolic structure where useful.
