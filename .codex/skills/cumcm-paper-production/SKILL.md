---
name: cumcm-paper-production
description: Build and operate an evidence-driven production system for CUMCM and similar mathematical modeling contest papers. Use when Codex must initialize a contest project, analyze a problem, select models, implement and run computations, generate traceable tables or figures, write or revise a paper from real outputs, maintain citations and AI-use records, or prepare reproducible submission materials.
---

# CUMCM Paper Production

Repository paths in this skill are logical paths relative to the current workspace root and follow the resolution convention in `AGENTS.md`.

Read `docs/README.md` for the authority matrix and `docs/standards/workspace-governance.md` for the operational baseline. Load only the additional authority documents triggered by the task. This skill executes the workflow; it does not define a second copy of thresholds, counts, schemas, formatting rules, or current official requirements.

## Execute the gated workflow

1. Inventory the statement, attachments, data, constraints, dependencies and requested outputs in `01-problem/problem-checklist.md`.
2. Read `resources/algorithm-library/index.md`, load only matching algorithm documents, and complete `WG-MODEL-001` before formal implementation.
3. Define the model, solver and validation strategy; implement it inside the project tree while enforcing `WG-DATA-001` and the reproducibility rules in workspace governance.
4. Run computations and save stable, machine-readable outputs, parameters and logs.
5. Complete the paper validation obligation `PW-VAL-001` using recorded runs or equally strong applicable evidence.
6. Register claims and sources under `WG-EVID-001` before concrete results or citations enter the paper.
7. Complete `PWL-GATE-001`, then write from verified evidence under `docs/standards/paper-writing.md`.
8. Maintain the AI ledger under `WG-AI-001` and apply `OFFICIAL-CUMCM-001` for current disclosure and submission rules.
9. Invoke the independent audit skill and clear `PQA-RELEASE-001` before release.

## Use bundled resources

- Run `scripts/init_cumcm_project.py` to create a normalized project tree.
- Read `resources/algorithm-library/index.md` before model selection and then load only matching algorithm documents.
- Read `docs/standards/evidence-contract.md` before producing concrete results or citations.
- Read `docs/guides/pre-writing-learning.md` immediately before paper drafting.
- Read `docs/standards/cumcm-current-rules.md` for current format and AI disclosure; reopen its official sources before a real submission.
- Follow the workspace `docs/standards/naming.md` for all stable artifact names.

## Stop conditions

Stop whenever `WG-MODEL-001`, `WG-EVID-001`, `PWL-GATE-001` or `PQA-RELEASE-001` blocks the next stage. Do not create concrete numerical claims without a successful run or valid derivation, and do not claim validation or performance without the evidence required by `PW-VAL-001`.
