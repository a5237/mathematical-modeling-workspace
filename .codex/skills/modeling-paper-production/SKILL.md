---
name: modeling-paper-production
description: Evidence-driven production of mathematical modeling contest papers across contest profiles. Use when Codex must initialize a contest project, analyze a problem, select models, run computations, produce traceable tables or figures, write or revise a paper from real outputs, maintain citations and AI-use records, or prepare reproducible submission.
---

# Mathematical Modeling Paper Production

Repository paths in this skill are logical paths relative to the current workspace root and follow the resolution convention in `AGENTS.md`.

For a full production workflow, read `docs/README.md` for the authority matrix and `docs/standards/workspace-governance.md` for cross-stage governance. Then load only the stage-specific authority documents triggered by the current step. Invoking this skill is not a prerequisite for ordinary local tasks. This skill executes the workflow; it does not define a second copy of thresholds, counts, schemas, formatting rules, or current official requirements.

Contest-specific rules, templates and submission requirements resolve through the current project's contest profile: read `00-admin/project.yaml`, map `contest` (or `profile` when present) to `config/contests/<profile>/`, and load that profile's `rules.md` when contest-specific requirements are in scope.

## Execute the gated workflow

1. Execute intake and initialization as defined by `docs/standards/workspace-governance.md` §3; use the bundled initializer for a new project.
2. Complete `WG-MODEL-001`, consulting `resources/algorithm-library/index.md` and only the matching algorithm resources; experiment artifacts remain governed by `WG-TEST-001`.
3. Implement data processing, models and formal entry points under `WG-DATA-001` and the remaining requirements of `docs/standards/data-reproducibility.md` and `docs/standards/modeling-execution.md`.
4. Run formal computations, save their stable outputs, and maintain `00-admin/artifact-map.yaml` under `WG-ROUTE-001`.
5. Complete `PW-VAL-001`, then register paper claims and sources under `WG-EVID-001`.
6. Complete `PWL-GATE-001`; draft and revise the initialized `06-paper/main.tex` under the paper-writing authority, adding `PW-FMT-001` whenever formatting is in scope.
7. Select, register, generate and review figures under `PW-FIG-001`.
8. Maintain `WG-AI-001` and apply the current contest profile's official baseline.
9. Form the production-to-audit handoff under `WG-RELEASE-001`; artifact routing and impact tracing are governed by `WG-ROUTE-001` and experiments by `WG-TEST-001`.
10. Hand the Release Candidate to the independent audit skill and clear `PQA-RELEASE-001` before release.

## Use bundled resources

- Run `scripts/init_modeling_project.py` for the `LAYOUT-001` recommended skeleton and project copies of the shared templates; `--contest` selects the contest profile (paper framework and contest rules).
- Use `tools/trace-artifact-impact.py` only as specified by `WG-ROUTE-001`.
- Use the initialized paper, artifact-map and figure-record files as implementations of their cited authorities; do not derive rules from template comments.
- Read `resources/algorithm-library/index.md` before model selection and then load only matching algorithm documents.
- Read `docs/standards/modeling-execution.md` for model selection, implementation, formal computation and `PW-VAL-001`.
- Read `docs/standards/data-reproducibility.md` for raw data, environment, runs, parameters, logs, seeds and reproducibility.
- Read `docs/standards/evidence-contract.md` before producing concrete results or citations.
- Read `docs/standards/paper-formatting.md` only when formatting, compiling or reviewing LaTeX, formulas, tables, fonts or page layout.
- Read `docs/standards/paper-figures.md` before selecting, generating or reviewing paper figures.
- When generating or aesthetically improving figures, read `docs/guides/scientific-figure-aesthetics.md` and the relevant reference-library manifest entries.
- Read `docs/guides/pre-writing-learning.md` immediately before paper drafting.
- Read the current contest profile's `config/contests/<profile>/rules.md` when current format or AI disclosure is in scope.
- Follow the workspace `docs/standards/naming.md` for all stable artifact names.

## Stop conditions

Stop on any blocking status from the control item required by the current step.
