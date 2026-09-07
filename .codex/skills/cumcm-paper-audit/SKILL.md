---
name: cumcm-paper-audit
description: Independently audit CUMCM and similar mathematical modeling papers against project evidence, reproducibility, citations, anonymity, format, and delivery requirements. Use when Codex must review, score, red-team, compliance-check, or release-gate a mathematical modeling paper without inventing fixes or trusting unsupported author claims.
---

# CUMCM Paper Audit

Act as an independent reviewer. Do not silently repair the paper while auditing it.

Repository paths in this skill are logical paths relative to the current workspace root and follow the resolution convention in `AGENTS.md`. Read `docs/README.md` for the authority matrix. This skill defines audit order only; thresholds, counts, schemas, official rules and paper requirements remain in their authority documents.

## Audit order

1. Confirm that the project is a frozen Release Candidate. Read the problem statement, triggered authority documents, problem checklist, model-selection record, learning record, paper, evidence and delivery inventory.
2. Run `scripts/audit_cumcm_project.py <project> --phase draft` for an early objective inventory. Missing release artifacts are advisory at this point; the script does not judge creativity, writing quality or visual merit.
3. From a clean directory or equivalent clean environment, execute the frozen documented entry point once. This single strong reproduction replaces any identical production-stage full rerun. Record the command, code/data/parameter fingerprint, exit status and key output comparison.
4. Verify `WG-MODEL-001` and `PWL-GATE-001` from substantive record contents; labels without evidence fail.
5. Trace paper claims and citations under `WG-EVID-001`, opening cited sources and confirming support for adjacent claims.
6. Check each subproblem against `PW-VAL-001`, verify core results, and check the reference list and in-text use against `PW-CITE-001` without inventing or padding sources.
7. Render the delivery PDF once, page by page. In the same pass inspect layout, margins, overflow, equations, tables, page counts and every figure under `PW-FIG-001`; do not create separate duplicate PDF and figure audits.
8. Check every delivery artifact for identity information under `docs/standards/paper-writing.md` section 15.3, enforce `OFFICIAL-CUMCM-001`, and compare the appendix file list with the delivery archive.
9. Classify findings under `docs/standards/paper-quality-audit.md` section 7. Block release on any critical or major finding caused by a hard error; a low competitiveness score alone is not a finding.
10. Write or update the single `07-review/final-audit.md` under `PQA-REPORT-001`, include the non-blocking competitiveness score, then run `scripts/audit_cumcm_project.py <project> --phase release-candidate` to verify the objective report contract and determine release under `PQA-RELEASE-001`.

## Final-stage impact review

If the audited PDF changes, update its hash. Re-run only the checks affected by the change, following `docs/standards/paper-quality-audit.md`: a typo or local non-paginating edit does not trigger model reproduction or a full figure audit; data, code, parameter or result changes do. Use `scripts/audit_cumcm_project.py <project> --phase final` after refreshing the report. An `IMPACTED` review must identify the previous full RC audit and the evidence that unchanged computation can be reused.

Never create missing experimental results, citations, checks, or sensitivity analyses as part of an audit. Report the absence and the exact evidence needed to clear it.
