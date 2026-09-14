---
name: cumcm-paper-audit
description: Independently audit CUMCM and similar mathematical modeling papers against project evidence, reproducibility, citations, anonymity, format, and delivery requirements. Use when Codex must review, score, red-team, compliance-check, or release-gate a mathematical modeling paper without inventing fixes or trusting unsupported author claims.
---

# CUMCM Paper Audit

Act as an independent reviewer. Do not silently repair the paper while auditing it.

Repository paths in this skill are logical paths relative to the current workspace root and follow the resolution convention in `AGENTS.md`. Read `docs/README.md` for the authority matrix. This skill defines audit order only; thresholds, counts, schemas, official rules and paper requirements remain in their authority documents.

## Audit order

1. Confirm that the project is a Release Candidate review snapshot. If present, open `00-admin/artifact-map.yaml` first and use its `common` plus per-question paths to locate upstream files; treat it only as a starting index, never as evidence or as a limit on independent review. For a legacy or stale map, fall back to searching only the relevant project directories; absence alone is not an audit failure. Then read the problem statement, problem checklist, model-selection record, learning record, paper, evidence and delivery inventory. A full RC audit loads the data/reproducibility, modeling/execution, evidence, paper-writing, paper-formatting, paper-figures, current-rules and quality-audit authorities; an impact review loads only the authorities touched by the change.
2. Run `scripts/audit_cumcm_project.py <project> --phase draft` for an early objective inventory. Missing release artifacts are advisory at this point; the script does not judge creativity, writing quality or visual merit.
3. Under `docs/standards/data-reproducibility.md`, execute the documented RC entry point once from a clean directory or equivalent clean environment. This single strong reproduction replaces any identical production-stage full rerun. Record the command, the required code/data/parameter filenames and existence states, stage completion, exit status and key output comparison; do not bind intermediate files by hash.
4. Verify `WG-MODEL-001` under `docs/standards/modeling-execution.md` and `PWL-GATE-001` from substantive record contents; labels without evidence fail.
5. Trace paper claims and citations under `WG-EVID-001`, opening cited sources and confirming support for adjacent claims. Reject any evidence source or generator rooted in the reserved `test/` sandbox, and check that paper numbers, tables and figures were not copied directly from exploratory test outputs; an adopted experiment must have a formal implementation, run and validation trail.
6. Check each subproblem against `PW-VAL-001` in the modeling/execution authority, verify core results, and check the reference list and in-text use against `PW-CITE-001` without inventing or padding sources.
7. Render the delivery PDF once, page by page. In the same pass inspect `PW-FMT-001` layout, margins, overflow, equations, tables and page counts plus every figure under `PW-FIG-001`; do not create separate duplicate PDF and figure audits.
8. Check every delivery artifact against the “匿名性” requirements in `docs/standards/paper-writing.md`, enforce `OFFICIAL-CUMCM-001`, and compare the appendix file list with the delivery archive.
9. Classify findings under `docs/standards/paper-quality-audit.md` section 7. Block release on any critical or major finding caused by a hard error; a low competitiveness score alone is not a finding.
10. Write or update the single `07-review/final-audit.md` under `PQA-REPORT-001`, include the non-blocking competitiveness score, then run `scripts/audit_cumcm_project.py <project> --phase release-candidate` to verify the objective report contract and determine release under `PQA-RELEASE-001`.

## Final-stage impact review

If the audited PDF changes, update its final-delivery hash. For substantive data, code, parameter, result or validation changes, run `tools/trace-artifact-impact.py <project> --changed <paths...>` to obtain an initial `STALE`/`RECHECK` inventory, then verify the actual review scope under `docs/standards/paper-quality-audit.md`; the trace never replaces reviewer judgment. A typo or local non-paginating edit does not trigger model reproduction or a full figure audit. Use `scripts/audit_cumcm_project.py <project> --phase final` after refreshing the report. An `IMPACTED` review must identify the previous full RC audit, list changed and required files with their existence states, explain why unchanged computation can be reused, and avoid intermediate file hashes.

Never create missing experimental results, citations, checks, or sensitivity analyses as part of an audit. Report the absence and the exact evidence needed to clear it.
