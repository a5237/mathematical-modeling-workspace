---
name: modeling-paper-audit
description: Independently audit mathematical modeling contest papers against project evidence, reproducibility, citations, anonymity, format, and delivery requirements. Use when Codex must review, score, red-team, compliance-check, or release-gate a mathematical modeling paper without inventing fixes or trusting unsupported author claims.
---

# Mathematical Modeling Paper Audit

Act as an independent reviewer. Do not silently repair the paper while auditing it.

Repository paths in this skill are logical paths relative to the current workspace root and follow the resolution convention in `AGENTS.md`. Read `docs/README.md` for the authority matrix. This skill defines audit order only; thresholds, counts, schemas, official rules and paper requirements remain in their authority documents.

Contest-specific rules resolve through the audited project's contest profile: read `00-admin/project.yaml`, map `contest` (or `profile` when present) to `config/contests/<profile>/`, and load that profile's `rules.md` when contest-specific requirements are in scope.

## Audit order

1. Confirm the audit phase under `docs/standards/paper-quality-audit.md`. Locate project inputs through `WG-ROUTE-001`, then load the full authority set for a full RC audit or only the affected authorities for an impact review.
2. Run `scripts/audit_modeling_project.py <project> --phase draft` for the early objective inventory.
3. Execute the RC reproduction and record its evidence under the data/reproducibility authority and the RC lifecycle defined by the audit standard.
4. Verify `WG-MODEL-001`, `PWL-GATE-001`, `WG-EVID-001`, `PW-VAL-001` and `PW-CITE-001` from substantive evidence.
5. Render the delivery PDF once and, in the same pass, execute `PW-FMT-001`, `PW-FIG-001`, the paper-writing anonymity control and the current contest profile's official baseline.
6. Classify findings and score competitiveness under the audit standard.
7. Write the single `PQA-REPORT-001` report, run `scripts/audit_modeling_project.py <project> --phase release-candidate`, and determine release only through `PQA-RELEASE-001`.

## Final-stage impact review

For a Final-stage change, obtain the initial impact inventory under `WG-ROUTE-001`, apply the audit standard's review-scope rules, refresh `PQA-REPORT-001`, and run `scripts/audit_modeling_project.py <project> --phase final`. This Skill adds no independent hash, reuse or `IMPACTED` criteria.

Never create missing experimental results, citations, checks, or sensitivity analyses as part of an audit. Report the absence and the exact evidence needed to clear it.
