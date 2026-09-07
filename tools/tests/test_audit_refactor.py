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
INIT_SCRIPT = WORKSPACE_ROOT / ".codex" / "skills" / "cumcm-paper-production" / "scripts" / "init_cumcm_project.py"
AUDIT_SCRIPT = WORKSPACE_ROOT / ".codex" / "skills" / "cumcm-paper-audit" / "scripts" / "audit_cumcm_project.py"
TEMP_ROOT = WORKSPACE_ROOT / "var" / "tmp"
sys.path.insert(0, str(WORKSPACE_ROOT / "tools"))

from control_contracts import load_workspace_contracts


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
        blocks = {
            "docs/standards/evidence-contract.md": (
                'claim_columns = ["a"]\nliterature_columns = ["b"]\n'
                'evidence_statuses = ["verified"]'
            ),
            "docs/standards/paper-writing.md": "body_word_minimum = 5000",
            "docs/standards/paper-quality-audit.md": (
                "body_page_minimum = 20\nbody_page_maximum = 30\n"
                "body_figure_minimum = 5\nbody_table_minimum = 3"
            ),
            "docs/guides/pre-writing-learning.md": (
                'learning_paper_minimum = 2\nlearning_complete_status = "COMPLETE"\n'
                'selection_complete_status = "COMPLETE"'
            ),
            "docs/standards/cumcm-current-rules.md": "paper_maximum_bytes = 20000000",
        }
        with tempfile.TemporaryDirectory(dir=TEMP_ROOT) as temporary:
            root = Path(temporary)
            for relative, block in blocks.items():
                path = root / relative
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(
                    "任意改写的自然语言和章节。\n\n```toml machine-contract\n"
                    + block
                    + "\n```\n\n另一段任意文字。\n",
                    encoding="utf-8",
                )
            contracts = load_workspace_contracts(root)
            self.assertEqual(contracts.body_word_minimum, 5000)
            self.assertEqual(contracts.learning_paper_minimum, 2)


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
            self.assertTrue((project / "03-models" / "model-selection.md").is_file())
            self.assertTrue((project / "00-admin" / "pre-writing-learning.md").is_file())
            self.assertTrue((project / "05-evidence" / "evidence-index.csv").is_file())
            self.assertTrue((project / "06-paper" / "main.tex").is_file())
            self.assertTrue((project / "00-admin" / "figure-selection-record.md").is_file())
            self.assertFalse((project / "07-review" / "final-audit.md").exists())


class ReleasePreflightTests(unittest.TestCase):
    def test_extra_directories_and_low_score_do_not_block_release(self) -> None:
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

            (project / "00-admin/runbook.md").write_text("运行入口已验证。", encoding="utf-8")
            (project / "01-problem/problem-checklist.md").write_text("题目与附件已核对。", encoding="utf-8")
            (project / "03-models/model-selection.md").write_text(
                "\n".join(
                    (
                        "selection_status: `COMPLETE`",
                        "completed_at: `2026-09-07`",
                        "candidates: 基准与候选已比较",
                        "suitability: 适用性已核对",
                        "selected_model: 已选用",
                        "validation: 已制定验证方案",
                        "resources/algorithm-library/01-优化算法说明.md",
                    )
                ),
                encoding="utf-8",
            )
            (project / "00-admin/pre-writing-learning.md").write_text(
                "\n".join(
                    (
                        "learning_status: `COMPLETE`",
                        "completed_at: `2026-09-07`",
                        "resources/paper-library/sample-a.md",
                        "resources/paper-library/sample-b.md",
                        "resources/algorithm-library/01-优化算法说明.md",
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
            (project / "07-review/final-audit.md").write_text(
                "\n".join(
                    (
                        "# 最终审查报告",
                        "- audit_date: `2026-09-07`",
                        "- audit_phase: `RELEASE_CANDIDATE`",
                        "- review_scope: `FULL`",
                        "- final_pdf: `08-delivery/paper.pdf`",
                        f"- final_pdf_sha256: `{digest}`",
                        "- body_word_count: `5000`",
                        "- body_page_range: `2-21`",
                        "- body_page_count: `20`",
                        "- body_figure_count: `5`",
                        "- body_table_count: `3`",
                        "- body_length_and_visual_count_gate: `PASS`",
                        "- official_rules_gate: `PASS`",
                        "- evidence_gate: `PASS`",
                        "- clean_reproduction_gate: `PASS`",
                        "- anonymity_gate: `PASS`",
                        "- delivery_gate: `PASS`",
                        "- open_critical: `0`",
                        "- open_major: `0`",
                        "- release_decision: `READY`",
                        "",
                        "## 竞争力评分",
                        "- total_score: 40",
                        "- grade: D",
                    )
                ),
                encoding="utf-8",
            )

            result = run(str(AUDIT_SCRIPT), str(project), "--phase", "release-candidate")
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("PASS (objective static preflight", result.stdout)

            compatibility = run(str(AUDIT_SCRIPT), str(project), "--phase", "release")
            self.assertEqual(compatibility.returncode, 0, compatibility.stdout + compatibility.stderr)

            result_artifact.unlink()
            blocked = run(str(AUDIT_SCRIPT), str(project), "--phase", "release-candidate")
            self.assertNotEqual(blocked.returncode, 0)
            self.assertIn("missing artifact", blocked.stdout)


if __name__ == "__main__":
    unittest.main()
