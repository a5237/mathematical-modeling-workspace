---
name: cumcm-paper-production
description: Build and operate an evidence-driven production system for CUMCM and similar mathematical modeling contest papers. Use when Codex must initialize a contest project, analyze a problem, select models, implement and run computations, generate traceable tables or figures, write or revise a paper from real outputs, maintain citations and AI-use records, or prepare reproducible submission materials.
---

# CUMCM Paper Production

Repository paths in this skill are logical paths relative to the current workspace root and follow the resolution convention in `AGENTS.md`.

For a full production workflow, read `docs/README.md` for the authority matrix and `docs/standards/workspace-governance.md` for cross-stage governance. Then load only the stage-specific authority documents triggered by the current step. Invoking this skill is not a prerequisite for ordinary local tasks. This skill executes the workflow; it does not define a second copy of thresholds, counts, schemas, formatting rules, or current official requirements.

## Execute the gated workflow

1. When the request arrives in `workspace/inbox/`, read the user request, statement and attachments, identify the contest/year/problem, run the initializer under `workspace/projects/`, route the statement to `01-problem/` and raw data to `02-data/raw/`, then clear the inbox only after verifying the project copy. This intake handoff remains mandatory even though ordinary inbox and project names are no longer machine gates.
2. Inventory the statement, attachments, data, constraints, dependencies and requested outputs in `01-problem/problem-checklist.md`.
3. Read `docs/standards/modeling-execution.md` and `resources/algorithm-library/index.md`, load only matching algorithm documents, and complete `WG-MODEL-001` before formal implementation. When candidate suitability is uncertain, use small-scale comparisons in `test/` as lightweight decision input; do not treat those runs as formal results or evidence.
4. Define the model, solver and validation strategy; implement it inside the project tree while enforcing `docs/standards/data-reproducibility.md`, including `WG-DATA-001`.
5. Run computations under the data/reproducibility rules and save stable, machine-readable outputs, parameters and logs. When a stable key file becomes useful to a downstream stage, add only its project-relative path to the affected `common` or question entry in `00-admin/artifact-map.yaml`.
6. Complete `PW-VAL-001` under `docs/standards/modeling-execution.md` using recorded runs or equally strong applicable evidence.
7. Register claims and sources under `WG-EVID-001` before concrete results or citations enter the paper; list only the useful `claim_id` and `citation_key` values in the affected artifact-map question entry, leaving all evidence metadata in the authoritative ledgers.
8. Complete `PWL-GATE-001`. Before drafting, read `common` plus the relevant question entries in `00-admin/artifact-map.yaml`, then copy `resources/templates/cumcm-paper-framework.tex` to `06-paper/main.tex` unless the initializer already created that project copy. Continue editing that single source under `docs/standards/paper-writing.md`; when editing LaTeX, formulas, tables or layout, also load `docs/standards/paper-formatting.md`. Preserve the fixed section framework and stateless-deliverable requirement instead of creating parallel drafts or extra top-level sections.
9. Select, register, generate and review paper figures under `docs/standards/paper-figures.md`. After chart type and encoding are fixed, use `docs/guides/scientific-figure-aesthetics.md` and only the relevant reference-library subset for optional aesthetic guidance. The only formal `PW-FIG-001` verdict is made on the final PDF.
10. Maintain material AI usage under `WG-AI-001` and apply `OFFICIAL-CUMCM-001`; do not log ordinary questions or every wording edit.
11. When the paper becomes a Release Candidate, mark the current main code, data processing, parameters and evidence as the review snapshot, then hand off to the independent audit skill. Intermediate gates record required artifact names, existence and stage completion rather than content hashes. If review exposes a possible algorithm, parameter or local implementation improvement, first compare it with the current solution in `test/` when a reduced experiment can answer the question. Only after deciding to adopt it, revise the affected formal paths, run `tools/trace-artifact-impact.py` with those formal changed paths, regenerate `STALE` artifacts, recheck only the reported `RECHECK` scopes, and form a new snapshot. The trace is a read-only starting inventory rather than a gate or audit verdict. Do not perform an extra full rerun when the audit's clean reproduction will execute the same entry point.
12. Clear `PQA-RELEASE-001` before release.

## Use bundled resources

- Run `scripts/init_cumcm_project.py` to create the recommended project tree, its lightweight non-stage `test/` sandbox, initialize `00-admin/artifact-map.yaml`, and copy `resources/templates/cumcm-paper-framework.tex` into it as `06-paper/main.tex`; projects may add or reorganize non-core directories afterward.
- Use `test/` only for exploratory small-sample, reduced-scale or local comparisons. Keep its organization proportional to the experiment, never register its contents in the artifact map or evidence ledger, and never cite or deliver them. If an experiment is adopted, reimplement and rerun it in the applicable formal stages before using its outputs downstream.
- Before downstream result analysis, writing or figure work, read only `common` and the relevant question entries in the artifact map. Treat it as a small navigation index, not a complete manifest, evidence ledger, or gate; do not add temporary files, every helper script, hashes, or stage status.
- Record only real cross-question dependencies in `depends_on_questions`. After a substantive upstream change, pass the changed project-relative paths explicitly to `tools/trace-artifact-impact.py`; do not infer a model rerun from a wording-only edit.
- Treat `06-paper/main.tex` as the only paper source after initialization; never overwrite an existing project paper with a fresh framework copy.
- Use the initialized `00-admin/figure-selection-record.md`, copied from `resources/templates/figure-selection-record.md`, under the registry rules in `docs/standards/paper-figures.md`.
- Read `resources/algorithm-library/index.md` before model selection and then load only matching algorithm documents.
- Read `docs/standards/modeling-execution.md` for model selection, implementation, formal computation and `PW-VAL-001`.
- Read `docs/standards/data-reproducibility.md` for raw data, environment, runs, parameters, logs, seeds and reproducibility.
- Read `docs/standards/evidence-contract.md` before producing concrete results or citations.
- Read `docs/standards/paper-formatting.md` only when formatting, compiling or reviewing LaTeX, formulas, tables, fonts or page layout.
- Read `docs/standards/paper-figures.md` before selecting, generating or reviewing paper figures.
- When generating or aesthetically improving figures, read `docs/guides/scientific-figure-aesthetics.md` and the reference-library manifest; transfer only recorded visual attributes and never let references override scientific structure.
- Read `docs/guides/pre-writing-learning.md` immediately before paper drafting.
- Read `docs/standards/cumcm-current-rules.md` for current format and AI disclosure; reopen its official sources before a real submission.
- Follow the workspace `docs/standards/naming.md` for all stable artifact names.

## Stop conditions

Stop whenever `WG-MODEL-001`, `WG-EVID-001` or `PWL-GATE-001` blocks the next production stage. At release, stop on a failed `PW-FIG-001` or `PQA-RELEASE-001`. `test/` never clears or weakens a gate. Do not create concrete numerical claims without a successful formal run or valid derivation, and do not claim validation or performance without the evidence required by `PW-VAL-001`.
