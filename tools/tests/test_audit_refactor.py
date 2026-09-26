from __future__ import annotations

import hashlib
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


WORKSPACE_ROOT = Path(__file__).resolve().parents[2]
PYTHON = sys.executable
LAYOUT_SCRIPT = WORKSPACE_ROOT / "tools" / "check-workspace-layout.py"
INIT_SCRIPT = WORKSPACE_ROOT / ".codex" / "skills" / "modeling-paper-production" / "scripts" / "init_modeling_project.py"
AUDIT_SCRIPT = WORKSPACE_ROOT / ".codex" / "skills" / "modeling-paper-audit" / "scripts" / "audit_modeling_project.py"
TEMP_ROOT = WORKSPACE_ROOT / "var" / "temp"
sys.path.insert(0, str(WORKSPACE_ROOT / "tools"))

from control_contracts import CONTRACT_BLOCK, CORE_DOCUMENTS, load_workspace_contracts


def run(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [PYTHON, *args],
        cwd=WORKSPACE_ROOT,
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        check=False,
    )


class LayoutTests(unittest.TestCase):
    def test_unknown_top_level_directory_is_allowed(self) -> None:
        with tempfile.TemporaryDirectory(dir=TEMP_ROOT) as temporary:
            root = Path(temporary)
            (root / "new-responsibility-layer").mkdir()
            result = run(str(LAYOUT_SCRIPT), "--root", str(root))
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_cache_directory_is_blocked(self) -> None:
        with tempfile.TemporaryDirectory(dir=TEMP_ROOT) as temporary:
            root = Path(temporary)
            (root / ".pytest_cache").mkdir()
            result = run(str(LAYOUT_SCRIPT), "--root", str(root))
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("runtime/cache directory", result.stdout)

    def test_project_artifact_burst_is_blocked(self) -> None:
        with tempfile.TemporaryDirectory(dir=TEMP_ROOT) as temporary:
            root = Path(temporary)
            for index in range(5):
                (root / f"result-{index}.csv").write_text("value\n1\n", encoding="utf-8")
            result = run(str(LAYOUT_SCRIPT), "--root", str(root))
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("project-artifact burst", result.stdout)


class ContractTests(unittest.TestCase):
    def test_contract_loader_ignores_natural_language(self) -> None:
        with tempfile.TemporaryDirectory(dir=TEMP_ROOT) as temporary:
            root = Path(temporary)
            for relative in CORE_DOCUMENTS:
                source = (WORKSPACE_ROOT / relative).read_text(encoding="utf-8")
                blocks = CONTRACT_BLOCK.findall(source)
                self.assertTrue(blocks, relative)
                path = root / relative
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(
                    "任意改写的自然语言和章节。\n\n```toml machine-contract\n"
                    + "\n\n".join(blocks)
                    + "\n```\n\n另一段任意文字。\n",
                    encoding="utf-8",
                )
            contracts = load_workspace_contracts(root)
            self.assertGreater(contracts.body_word_minimum, 0)
            self.assertGreater(contracts.body_figure_minimum, 0)
            self.assertGreater(contracts.body_table_minimum, 0)
            self.assertGreater(contracts.learning_paper_minimum, 0)
            self.assertIn("sandbox", contracts.recommended_project_directories)
            self.assertEqual(contracts.artifact_impact_defaults["results"]["effect"], "STALE")


class IntakeWorkflowTests(unittest.TestCase):
    def test_initializer_preserves_inbox_to_project_destinations(self) -> None:
        with tempfile.TemporaryDirectory(dir=TEMP_ROOT) as temporary:
            root = Path(temporary)
            inbox = root / "inbox" / "new-request"
            projects = root / "projects"
            inbox.mkdir(parents=True)
            (inbox / "request.md").write_text("题目要求", encoding="utf-8")
            (inbox / "statement.pdf").write_bytes(b"statement")
            (inbox / "data.xlsx").write_bytes(b"data")

            result = run(
                str(INIT_SCRIPT),
                "--root",
                str(projects),
                "--contest",
                "cumcm",
                "--year",
                "2026",
                "--problem",
                "a",
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            project = projects / "cumcm-2026-a"

            shutil.copy2(inbox / "statement.pdf", project / "01-problem" / "attachments" / "statement.pdf")
            shutil.copy2(inbox / "data.xlsx", project / "02-data" / "raw" / "data.xlsx")
            shutil.copy2(inbox / "request.md", project / "01-problem" / "request.md")

            self.assertTrue((project / "01-problem" / "problem-checklist.md").is_file())
            model_selection = project / "03-models" / "model-selection.md"
            self.assertTrue(model_selection.is_file())
            self.assertIn(
                "WG-MODEL-001",
                model_selection.read_text(encoding="utf-8"),
            )
            self.assertTrue((project / "00-admin" / "pre-writing-learning.md").is_file())
            artifact_map = project / "00-admin" / "artifact-map.yaml"
            self.assertTrue(artifact_map.is_file())
            artifact_map_text = artifact_map.read_text(encoding="utf-8")
            self.assertIn('project_id: "cumcm-2026-a"', artifact_map_text)
            self.assertIn("questions:\n  q01:", artifact_map_text)
            self.assertNotIn("impact_defaults:", artifact_map_text)
            self.assertIn("paper_assets:", artifact_map_text)
            self.assertIn("depends_on_questions: []", artifact_map_text)
            self.assertNotIn("__PROJECT_ID__", artifact_map_text)
            self.assertTrue((project / "05-evidence" / "evidence-index.csv").is_file())
            self.assertTrue((project / "06-paper" / "main.tex").is_file())
            self.assertTrue((project / "00-admin" / "figure-selection-record.md").is_file())
            self.assertTrue((project / "sandbox" / "README.md").is_file())
            self.assertIn(
                "WG-TEST-001",
                (project / "sandbox" / "README.md").read_text(encoding="utf-8"),
            )
            self.assertFalse((project / "07-review" / "final-audit.md").exists())


class ReleasePreflightTests(unittest.TestCase):
    def test_reserved_sandbox_artifact_cannot_be_formal_evidence(self) -> None:
        with tempfile.TemporaryDirectory(dir=TEMP_ROOT) as temporary:
            project = Path(temporary) / "project"
            (project / "05-evidence").mkdir(parents=True)
            artifact = project / "sandbox" / "q01-fast-check" / "result.json"
            artifact.parent.mkdir(parents=True)
            (project / "00-admin").mkdir(exist_ok=True)
            (project / "00-admin/project.yaml").write_text(
                "project_id: fixture\ncontest: cumcm\nprofile: cumcm\nyear: 2026\nproblem: a\nstatus: intake\n",
                encoding="utf-8",
            )
            artifact.write_text('{"value": 1}', encoding="utf-8")
            (project / "05-evidence/evidence-index.csv").write_text(
                "claim_id,question_id,claim,evidence_type,source_path,generator,generated_at,status\n"
                "C-Q01-001,q01,核心结果,metric,sandbox/q01-fast-check/result.json,sandbox/q01-fast-check/run.py,2026-09-14T00:00:00,verified\n",
                encoding="utf-8",
            )

            result = run(str(AUDIT_SCRIPT), str(project), "--phase", "draft")
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("reserved sandbox/ artifact is non-authoritative", result.stdout)
            self.assertIn("generator points into reserved sandbox/", result.stdout)

    def test_extra_directories_and_low_score_do_not_block_release(self) -> None:
        contracts = load_workspace_contracts(WORKSPACE_ROOT, contest="cumcm")
        with tempfile.TemporaryDirectory(dir=TEMP_ROOT) as temporary:
            project = Path(temporary) / "project with flexible layout"
            for relative in (
                "00-admin",
                "01-problem",
                "03-models",
                "05-evidence",
                "06-paper",
                "07-review",
                "08-delivery",
                "experiments/benchmarks",
                "simulations",
            ):
                (project / relative).mkdir(parents=True, exist_ok=True)

            (project / "00-admin/project.yaml").write_text(
                "project_id: fixture\ncontest: cumcm\nprofile: cumcm\nyear: 2026\nproblem: a\nstatus: intake\n",
                encoding="utf-8",
            )
            (project / "00-admin/runbook.md").write_text("运行入口已验证。", encoding="utf-8")
            (project / "01-problem/problem-checklist.md").write_text("题目与附件已核对。", encoding="utf-8")
            (project / "03-models/model-selection.md").write_text(
                "\n".join(
                    (
                        "selection_status: `COMPLETE`",
                        "stage_record: 模型选择已由独立审查核对",
                    )
                ),
                encoding="utf-8",
            )
            (project / "00-admin/pre-writing-learning.md").write_text(
                "\n".join(
                    (
                        "learning_status: `COMPLETE`",
                        "stage_record: 写作前学习已由独立审查核对",
                    )
                ),
                encoding="utf-8",
            )
            result_artifact = project / "experiments" / "benchmarks" / "result.json"
            result_artifact.write_text('{"value": 1}', encoding="utf-8")
            (project / "05-evidence/evidence-index.csv").write_text(
                "claim_id,question_id,claim,evidence_type,source_path,generator,generated_at,status\n"
                "claim-1,part-a,核心结果,metric,experiments/benchmarks/result.json,run.py,2026-09-07T00:00:00,verified\n",
                encoding="utf-8",
            )
            (project / "05-evidence/literature-ledger.csv").write_text(
                "citation_key,title,authors,year,doi_or_url,retrieved_at,used_in,verified\n",
                encoding="utf-8",
            )
            (project / "05-evidence/ai-tool-log.md").write_text("无未披露的实质使用。", encoding="utf-8")
            (project / "06-paper/main.tex").write_text("正式论文源", encoding="utf-8")
            (project / "08-delivery/file-list.md").write_text("paper.pdf：论文", encoding="utf-8")
            pdf = project / "08-delivery/paper.pdf"
            pdf.write_bytes(b"synthetic-pdf-for-static-preflight")
            digest = hashlib.sha256(pdf.read_bytes()).hexdigest()
            body_start_page = 2
            body_end_page = body_start_page + contracts.body_page_minimum - 1
            (project / "07-review/final-audit.md").write_text(
                "\n".join(
                    (
                        "# 最终审查报告",
                        "- audit_date: `2026-09-07`",
                        f"- audit_phase: `{contracts.release_candidate_phase_value}`",
                        f"- review_scope: `{contracts.release_candidate_review_scopes[0]}`",
                        "- final_pdf: `08-delivery/paper.pdf`",
                        f"- final_pdf_sha256: `{digest}`",
                        f"- body_word_count: `{contracts.body_word_minimum}`",
                        f"- body_page_range: `{body_start_page}-{body_end_page}`",
                        f"- body_page_count: `{contracts.body_page_minimum}`",
                        f"- body_figure_count: `{contracts.body_figure_minimum}`",
                        f"- body_table_count: `{contracts.body_table_minimum}`",
                        f"- body_length_and_visual_count_gate: `{contracts.final_audit_pass_status}`",
                        f"- official_rules_gate: `{contracts.final_audit_pass_status}`",
                        f"- evidence_gate: `{contracts.final_audit_pass_status}`",
                        f"- clean_reproduction_gate: `{contracts.release_candidate_reproduction_statuses[0]}`",
                        f"- anonymity_gate: `{contracts.final_audit_pass_status}`",
                        f"- delivery_gate: `{contracts.final_audit_pass_status}`",
                        f"- open_critical: `{contracts.final_audit_no_open_findings_value}`",
                        f"- open_major: `{contracts.final_audit_no_open_findings_value}`",
                        f"- release_decision: `{contracts.release_ready_status}`",
                        "",
                        "## 竞争力评分",
                        "- total_score: 40",
                        "- grade: D",
                    )
                ),
                encoding="utf-8",
            )

            self.assertFalse((project / "00-admin/artifact-map.yaml").exists())
            result = run(str(AUDIT_SCRIPT), str(project), "--phase", "release-candidate")
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("PASS (objective static preflight", result.stdout)

            code = project / "experiments" / "run.py"
            code.write_text("print('revised implementation')\n", encoding="utf-8")
            revised = run(str(AUDIT_SCRIPT), str(project), "--phase", "release-candidate")
            self.assertEqual(revised.returncode, 0, revised.stdout + revised.stderr)

            compatibility = run(str(AUDIT_SCRIPT), str(project), "--phase", "release")
            self.assertEqual(compatibility.returncode, 0, compatibility.stdout + compatibility.stderr)

            result_artifact.unlink()
            blocked = run(str(AUDIT_SCRIPT), str(project), "--phase", "release-candidate")
            self.assertNotEqual(blocked.returncode, 0)
            self.assertIn("missing artifact", blocked.stdout)


if __name__ == "__main__":
    unittest.main()
