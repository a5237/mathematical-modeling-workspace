from __future__ import annotations

import csv
import json
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import yaml


WORKSPACE_ROOT = Path(__file__).resolve().parents[2]
PYTHON = sys.executable
TEMP_ROOT = WORKSPACE_ROOT / "var" / "temp"
INIT_SCRIPT = (
    WORKSPACE_ROOT
    / ".codex"
    / "skills"
    / "modeling-paper-production"
    / "scripts"
    / "init_modeling_project.py"
)
TRACE_SCRIPT = WORKSPACE_ROOT / "tools" / "trace-artifact-impact.py"
AUDIT_SCRIPT = (
    WORKSPACE_ROOT
    / ".codex"
    / "skills"
    / "modeling-paper-audit"
    / "scripts"
    / "audit_modeling_project.py"
)
LAYOUT_SCRIPT = WORKSPACE_ROOT / "tools" / "check-workspace-layout.py"
sys.path.insert(0, str(WORKSPACE_ROOT / "tools"))

from control_contracts import load_workspace_contracts


def run(*args: str, cwd: Path = WORKSPACE_ROOT) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [PYTHON, *args],
        cwd=cwd,
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        check=False,
    )


def impact_ids(items: list[dict[str, object]]) -> set[str]:
    return {f"{item['scope']}.{item['category']}" for item in items}


CONTROL_ID = re.compile(r"\b(?:LAYOUT|WG|PW|PWL|PQA|OFFICIAL)-[A-Z]+-\d{3}\b")
CONTROL_DEFINITION = re.compile(
    r"^(?:>\s*control_id:\s*`(?P<meta>[^`]+)`|#{1,6}\s+.*?`(?P<heading>(?:LAYOUT|WG|PW|PWL|PQA|OFFICIAL)-[A-Z]+-\d{3})`)",
    re.MULTILINE,
)


def specification_files() -> list[Path]:
    roots = (
        WORKSPACE_ROOT / "docs",
        WORKSPACE_ROOT / ".codex" / "skills",
        WORKSPACE_ROOT / "resources" / "templates",
        WORKSPACE_ROOT / "config",
    )
    files = [WORKSPACE_ROOT / "AGENTS.md", WORKSPACE_ROOT / "README.md"]
    for root in roots:
        files.extend(
            path
            for path in root.rglob("*")
            if path.suffix.lower() in {".md", ".tex", ".yaml", ".yml"}
        )
    return files


def control_inventory() -> tuple[set[str], dict[str, list[str]]]:
    references: set[str] = set()
    definitions: dict[str, list[str]] = {}
    for path in specification_files():
        text = path.read_text(encoding="utf-8", errors="replace")
        references.update(CONTROL_ID.findall(text))
        matches = CONTROL_DEFINITION.finditer(text) if path.suffix.lower() == ".md" else ()
        for match in matches:
            control_id = match.group("meta") or match.group("heading")
            if CONTROL_ID.fullmatch(control_id):
                definitions.setdefault(control_id, []).append(
                    path.relative_to(WORKSPACE_ROOT).as_posix()
                )
    return references, definitions


class V2InfrastructureSmokeTest(unittest.TestCase):
    def test_real_end_to_end_infrastructure_path(self) -> None:
        contracts = load_workspace_contracts(WORKSPACE_ROOT)
        references, definitions = control_inventory()
        self.assertEqual(
            sorted(references),
            sorted(definitions),
            "every cited control must have one explicit authority definition",
        )
        self.assertTrue(
            all(len(paths) == 1 for paths in definitions.values()),
            f"duplicate control definitions: {definitions}",
        )
        temporary_root: Path | None = None

        with tempfile.TemporaryDirectory(dir=TEMP_ROOT, prefix="v2-smoke-") as temporary:
            temporary_root = Path(temporary)
            projects = temporary_root / "projects"
            initialized = run(
                str(INIT_SCRIPT),
                "--root",
                str(projects),
                "--contest",
                "cumcm",
                "--year",
                "2099",
                "--problem",
                "e2e",
            )
            self.assertEqual(initialized.returncode, 0, initialized.stdout + initialized.stderr)
            project = projects / "cumcm-2099-e2e"

            for relative in contracts.recommended_project_directories:
                self.assertTrue((project / relative).is_dir(), relative)

            map_path = project / "00-admin" / "artifact-map.yaml"
            artifact_map = yaml.safe_load(map_path.read_text(encoding="utf-8"))
            self.assertEqual(artifact_map["project_id"], project.name)
            self.assertNotIn("impact_defaults", artifact_map)
            self.assertTrue(set(contracts.artifact_index_names).issubset(artifact_map["indexes"]))
            q01 = artifact_map["questions"]["q01"]
            self.assertTrue(set(contracts.artifact_path_categories).issubset(q01))
            self.assertTrue(
                set(contracts.artifact_question_evidence_fields).issubset(q01["evidence"])
            )
            self.assertTrue((project / "sandbox" / "README.md").is_file())
            figure_record = (project / "00-admin" / "figure-selection-record.md").read_text(
                encoding="utf-8"
            )
            self.assertNotIn("__FIGURE_", figure_record)
            self.assertIn(contracts.figure_initial_status, figure_record)

            data_path = project / "02-data" / "processed" / "q01-input.csv"
            data_path.write_text("value\n1\n2\n3\n", encoding="utf-8")
            model_path = project / "03-models" / "q01" / "q01-run.py"
            model_path.write_text(
                "from pathlib import Path\n"
                "import csv, json\n"
                "root = Path.cwd()\n"
                "source = root / '02-data/processed/q01-input.csv'\n"
                "with source.open(encoding='utf-8', newline='') as handle:\n"
                "    values = [float(row['value']) for row in csv.DictReader(handle)]\n"
                "target = root / '04-results/metrics/q01-metrics.json'\n"
                "target.write_text(json.dumps({'count': len(values), 'sum': sum(values)}), encoding='utf-8')\n",
                encoding="utf-8",
            )
            model_run = run("03-models/q01/q01-run.py", cwd=project)
            self.assertEqual(model_run.returncode, 0, model_run.stdout + model_run.stderr)

            result_path = project / "04-results" / "metrics" / "q01-metrics.json"
            self.assertEqual(json.loads(result_path.read_text(encoding="utf-8"))["sum"], 6.0)
            validation_path = project / "04-results" / "metrics" / "q01-validation.json"
            validation_path.write_text('{"status":"PASS"}\n', encoding="utf-8")
            paper_asset = project / "06-paper" / "tables" / "q01-summary.csv"
            paper_asset.write_text("metric,value\nsum,6\n", encoding="utf-8")
            exploratory = project / "sandbox" / "q01-fast-check" / "result.json"
            exploratory.parent.mkdir(parents=True)
            exploratory.write_text('{"sum":6}\n', encoding="utf-8")

            q01.update(
                {
                    "data": [data_path.relative_to(project).as_posix()],
                    "code": [model_path.relative_to(project).as_posix()],
                    "results": [result_path.relative_to(project).as_posix()],
                    "validation": [validation_path.relative_to(project).as_posix()],
                    "paper_assets": [paper_asset.relative_to(project).as_posix()],
                }
            )
            q01["evidence"]["claim_ids"] = ["C-Q01-001"]
            map_path.write_text(
                yaml.safe_dump(artifact_map, allow_unicode=True, sort_keys=False),
                encoding="utf-8",
            )

            formal_trace = run(
                str(TRACE_SCRIPT),
                str(project),
                "--changed",
                data_path.relative_to(project).as_posix(),
                "--format",
                "json",
            )
            self.assertEqual(formal_trace.returncode, 0, formal_trace.stdout + formal_trace.stderr)
            formal_report = json.loads(formal_trace.stdout)
            self.assertEqual(formal_report["mode"], "mapped")
            self.assertTrue(
                {"q01.results", "q01.validation", "q01.paper_assets"}.issubset(
                    impact_ids(formal_report["stale"])
                )
            )
            self.assertTrue(
                {"q01.evidence", "q01.paper", "q01.review", "q01.delivery"}.issubset(
                    impact_ids(formal_report["recheck"])
                )
            )

            test_trace = run(
                str(TRACE_SCRIPT),
                str(project),
                "--changed",
                exploratory.relative_to(project).as_posix(),
                "--format",
                "json",
            )
            self.assertEqual(test_trace.returncode, 0, test_trace.stdout + test_trace.stderr)
            test_report = json.loads(test_trace.stdout)
            self.assertEqual(test_report["mode"], "exploratory")
            self.assertEqual(test_report["stale"], [])
            self.assertEqual(test_report["recheck"], [])

            evidence_path = project / "05-evidence" / "evidence-index.csv"
            with evidence_path.open("w", encoding="utf-8", newline="") as handle:
                writer = csv.DictWriter(handle, fieldnames=contracts.claim_columns)
                writer.writeheader()
                writer.writerow(
                    {
                        "claim_id": "C-Q01-001",
                        "question_id": "q01",
                        "claim": "最小模型求和结果为 6",
                        "evidence_type": "metric",
                        "source_path": result_path.relative_to(project).as_posix(),
                        "generator": model_path.relative_to(project).as_posix(),
                        "generated_at": "2099-01-01T00:00:00",
                        "status": "verified",
                    }
                )

            audit = run(str(AUDIT_SCRIPT), str(project), "--phase", "draft")
            self.assertEqual(audit.returncode, 0, audit.stdout + audit.stderr)
            self.assertIn("PASS (objective static preflight", audit.stdout)

            layout = run(str(LAYOUT_SCRIPT), "--root", str(WORKSPACE_ROOT))
            self.assertEqual(layout.returncode, 0, layout.stdout + layout.stderr)
            self.assertIn("RESULT: PASS", layout.stdout)

        self.assertIsNotNone(temporary_root)
        self.assertFalse(temporary_root.exists(), "temporary smoke project was not removed")


if __name__ == "__main__":
    unittest.main()
