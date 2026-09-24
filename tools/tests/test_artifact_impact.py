from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import yaml


WORKSPACE_ROOT = Path(__file__).resolve().parents[2]
PYTHON = sys.executable
SCRIPT = WORKSPACE_ROOT / "tools" / "trace-artifact-impact.py"
TEMPLATE = WORKSPACE_ROOT / "resources" / "templates" / "artifact-map.yaml"
TEMP_ROOT = WORKSPACE_ROOT / "var" / "temp"


def run(project: Path, *changed: str, output_format: str = "json") -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [
            PYTHON,
            str(SCRIPT),
            str(project),
            "--changed",
            *changed,
            "--format",
            output_format,
        ],
        cwd=WORKSPACE_ROOT,
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        check=False,
    )


def question(
    question_id: str,
    *,
    depends_on_questions: list[str] | None = None,
) -> dict[str, object]:
    return {
        "data": [f"02-data/processed/{question_id}-input.csv"],
        "code": [f"03-models/{question_id}/{question_id}-run.py"],
        "parameters": [f"03-models/{question_id}/{question_id}-parameters.yaml"],
        "results": [f"04-results/metrics/{question_id}-metrics.json"],
        "validation": [f"04-results/metrics/{question_id}-validation.json"],
        "paper_assets": [f"06-paper/figures/{question_id}-figure-001.png"],
        "evidence": {
            "claim_ids": [f"C-{question_id.upper()}-001"],
            "citation_keys": [f"author-2026-{question_id}"],
        },
        "depends_on_questions": depends_on_questions or [],
    }


def write_map(project: Path, questions: dict[str, object], common: dict[str, object] | None = None) -> Path:
    data = yaml.safe_load(TEMPLATE.read_text(encoding="utf-8"))
    data["project_id"] = project.name
    data["questions"] = questions
    if common is not None:
        data["common"] = common
    path = project / "00-admin" / "artifact-map.yaml"
    path.parent.mkdir(parents=True)
    path.write_text(
        yaml.safe_dump(data, allow_unicode=True, sort_keys=False), encoding="utf-8"
    )
    return path


def node_ids(items: list[dict[str, object]]) -> set[str]:
    return {f"{item['scope']}.{item['category']}" for item in items}


class ArtifactImpactTests(unittest.TestCase):
    def test_transitive_and_cross_question_impact_is_split_by_action(self) -> None:
        with tempfile.TemporaryDirectory(dir=TEMP_ROOT) as temporary:
            project = Path(temporary) / "project"
            project.mkdir()
            map_path = write_map(
                project,
                {
                    "q01": question("q01"),
                    "q02": question("q02", depends_on_questions=["q01.results"]),
                    "q03": question("q03"),
                },
            )
            before = map_path.read_bytes()

            result = run(project, "02-data/processed/q01-input.csv")
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            report = json.loads(result.stdout)

            self.assertEqual(report["mode"], "mapped")
            self.assertEqual(map_path.read_bytes(), before)
            stale = node_ids(report["stale"])
            recheck = node_ids(report["recheck"])
            self.assertTrue(
                {
                    "q01.results",
                    "q01.validation",
                    "q01.paper_assets",
                    "q02.results",
                    "q02.validation",
                    "q02.paper_assets",
                }.issubset(stale)
            )
            self.assertTrue(
                {
                    "q01.evidence",
                    "q01.paper",
                    "q01.review",
                    "q01.delivery",
                    "q02.evidence",
                    "q02.paper",
                    "q02.review",
                    "q02.delivery",
                }.issubset(recheck)
            )
            self.assertFalse(any(item.startswith("q03.") for item in stale | recheck))
            q01_result = next(item for item in report["stale"] if item["scope"] == "q01" and item["category"] == "results")
            self.assertEqual(q01_result["paths"], ["04-results/metrics/q01-metrics.json"])
            self.assertEqual(report["matched"][0]["source"], "artifact-map")

    def test_common_change_affects_every_mapped_question(self) -> None:
        with tempfile.TemporaryDirectory(dir=TEMP_ROOT) as temporary:
            project = Path(temporary) / "project"
            project.mkdir()
            common = {
                "data": ["02-data/processed/common-input.csv"],
                "code": [],
                "parameters": [],
                "results": ["04-results/metrics/common-metrics.json"],
                "validation": [],
                "paper_assets": [],
            }
            write_map(project, {"q01": question("q01"), "q02": question("q02")}, common)

            result = run(project, "02-data/processed/common-input.csv")
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            report = json.loads(result.stdout)
            stale = node_ids(report["stale"])
            self.assertTrue(
                {"common.results", "q01.results", "q02.results"}.issubset(stale)
            )

    def test_missing_map_uses_conservative_path_inference(self) -> None:
        with tempfile.TemporaryDirectory(dir=TEMP_ROOT) as temporary:
            project = Path(temporary) / "legacy-project"
            project.mkdir()

            result = run(project, "03-models/q03/q03-run.py")
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            report = json.loads(result.stdout)

            self.assertEqual(report["mode"], "inferred")
            self.assertIn("q03.results", node_ids(report["stale"]))
            self.assertIn("q03.paper", node_ids(report["recheck"]))
            self.assertTrue(any("artifact map is missing" in item for item in report["warnings"]))

    def test_changed_path_cannot_escape_project(self) -> None:
        with tempfile.TemporaryDirectory(dir=TEMP_ROOT) as temporary:
            project = Path(temporary) / "project"
            project.mkdir()

            result = run(project, "../outside.csv")
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("escapes the project root", result.stderr)

    def test_reserved_sandbox_change_does_not_enter_formal_impact_chain(self) -> None:
        with tempfile.TemporaryDirectory(dir=TEMP_ROOT) as temporary:
            project = Path(temporary) / "project"
            project.mkdir()
            write_map(project, {"q01": question("q01")})

            result = run(project, "sandbox/q01-solver-comparison/result.json")
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            report = json.loads(result.stdout)

            self.assertEqual(report["mode"], "exploratory")
            self.assertEqual(report["stale"], [])
            self.assertEqual(report["recheck"], [])
            self.assertEqual(report["matched"][0]["source"], "reserved-sandbox")
            self.assertTrue(any("no formal impact" in item for item in report["warnings"]))

    def test_legacy_map_cannot_override_authority_impact_rules(self) -> None:
        with tempfile.TemporaryDirectory(dir=TEMP_ROOT) as temporary:
            project = Path(temporary) / "project"
            project.mkdir()
            map_path = write_map(project, {"q01": question("q01")})
            artifact_map = yaml.safe_load(map_path.read_text(encoding="utf-8"))
            artifact_map["impact_defaults"] = {
                "results": {"depends_on": ["paper"], "effect": "RECHECK"}
            }
            map_path.write_text(
                yaml.safe_dump(artifact_map, allow_unicode=True, sort_keys=False),
                encoding="utf-8",
            )

            result = run(project, "02-data/processed/q01-input.csv")
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            report = json.loads(result.stdout)

            self.assertIn("q01.results", node_ids(report["stale"]))
            self.assertTrue(
                any("WG-ROUTE-001 is authoritative" in item for item in report["warnings"])
            )


if __name__ == "__main__":
    unittest.main()
