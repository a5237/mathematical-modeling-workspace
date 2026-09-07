---
name: cumcm-paper-production
description: Build and operate an evidence-driven production system for CUMCM and similar mathematical modeling contest papers. Use when Codex must initialize a contest project, analyze a problem, select models, implement and run computations, generate traceable tables or figures, write or revise a paper from real outputs, maintain citations and AI-use records, or prepare reproducible submission materials.
---

# CUMCM Paper Production

Repository paths in this skill are logical paths relative to the current workspace root and follow the resolution convention in `AGENTS.md`.

Read `docs/README.md` for the authority matrix and `docs/standards/workspace-governance.md` for the operational baseline. Load only the additional authority documents triggered by the task. This skill executes the workflow; it does not define a second copy of thresholds, counts, schemas, formatting rules, or current official requirements.

## Execute the gated workflow

1. When the request arrives in `workspace/inbox/`, read the user request, statement and attachments, identify the contest/year/problem, run the initializer under `workspace/projects/`, route the statement to `01-problem/` and raw data to `02-data/raw/`, then clear the inbox only after verifying the project copy. This intake handoff remains mandatory even though ordinary inbox and project names are no longer machine gates.
2. Inventory the statement, attachments, data, constraints, dependencies and requested outputs in `01-problem/problem-checklist.md`.
3. Read `resources/algorithm-library/index.md`, load only matching algorithm documents, and complete `WG-MODEL-001` before formal implementation.
4. Define the model, solver and validation strategy; implement it inside the project tree while enforcing `WG-DATA-001` and the reproducibility rules in workspace governance.
5. Run computations and save stable, machine-readable outputs, parameters and logs.
6. Complete the paper validation obligation `PW-VAL-001` using recorded runs or equally strong applicable evidence.
7. Register claims and sources under `WG-EVID-001` before concrete results or citations enter the paper.
8. Complete `PWL-GATE-001`. Before drafting, copy `resources/templates/cumcm-paper-framework.tex` to `06-paper/main.tex` unless the initializer already created that project copy. Continue editing that single source under `docs/standards/paper-writing.md`; preserve its fixed section framework and stateless-deliverable requirement instead of creating parallel drafts or extra top-level sections.
9. Select and generate paper figures under `docs/standards/paper-figures.md`. Register ordinary figures once in the lightweight figure registry; add detail only for potentially misleading transformations. Never prefer a simpler, lower-information chart to reduce implementation or review work. After chart type and encoding are fixed, use a small relevant subset of `resources/figure-style-library/` only as optional aesthetic guidance. The only formal `PW-FIG-001` verdict is made on the final PDF.
10. Maintain material AI usage under `WG-AI-001` and apply `OFFICIAL-CUMCM-001`; do not log ordinary questions or every wording edit.
11. When the paper becomes a Release Candidate, freeze the main code, data processing, parameters and evidence, then hand off to the independent audit skill. Do not perform an extra full rerun when the audit's clean reproduction will execute the same frozen entry point.
12. Clear `PQA-RELEASE-001` before release.

## Use bundled resources

- Run `scripts/init_cumcm_project.py` to create the recommended project tree and copy `resources/templates/cumcm-paper-framework.tex` into it as `06-paper/main.tex`; projects may add or reorganize non-core directories afterward.
- Treat `06-paper/main.tex` as the only paper source after initialization; never overwrite an existing project paper with a fresh framework copy.
- Use the initialized `00-admin/figure-selection-record.md`, copied from `resources/templates/figure-selection-record.md`, as a lightweight registry. Complex scientific charts do not require extra records merely because they are complex.
- Read `resources/algorithm-library/index.md` before model selection and then load only matching algorithm documents.
- Read `docs/standards/evidence-contract.md` before producing concrete results or citations.
- Read `docs/standards/paper-figures.md` before selecting, generating or reviewing paper figures.
- When generating or aesthetically improving figures, read `docs/guides/scientific-figure-aesthetics.md` and the reference-library manifest; transfer only recorded visual attributes and never let references override scientific structure.
- Read `docs/guides/pre-writing-learning.md` immediately before paper drafting.
- Read `docs/standards/cumcm-current-rules.md` for current format and AI disclosure; reopen its official sources before a real submission.
- Follow the workspace `docs/standards/naming.md` for all stable artifact names.

## Stop conditions

Stop whenever `WG-MODEL-001`, `WG-EVID-001` or `PWL-GATE-001` blocks the next production stage. At release, stop on a failed `PW-FIG-001` or `PQA-RELEASE-001`. Do not create concrete numerical claims without a successful run or valid derivation, and do not claim validation or performance without the evidence required by `PW-VAL-001`.
