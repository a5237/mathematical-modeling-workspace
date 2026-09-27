from __future__ import annotations

import hashlib
import re
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

from control_contracts import (
    CONTRACT_BLOCK,
    CORE_DOCUMENTS,
    ContractError,
    check_profile_registry,
    load_workspace_contracts,
)


def core_scaffold(root: Path) -> Path:
    """Copy the real Core contract blocks into an otherwise empty workspace root."""

    for relative in CORE_DOCUMENTS:
        source = (WORKSPACE_ROOT / relative).read_text(encoding="utf-8")
        blocks = CONTRACT_BLOCK.findall(source)
        assert blocks, relative
        path = root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            "任意改写的自然语言和章节。\n\n```toml machine-contract\n"
            + "\n\n".join(blocks)
            + "\n```\n\n另一段任意文字。\n",
            encoding="utf-8",
        )
    return root


def write_profile(
    root: Path,
    name: str,
    contests: tuple[str, ...],
    contract_keys: tuple[str, ...] = (),
    rules: str = "# 规则\n",
    extra_files: dict[str, str] | None = None,
) -> Path:
    profile = root / "config" / "contests" / name
    profile.mkdir(parents=True)
    profile_yaml = "contests:\n" + "".join(f"  - {item}\n" for item in contests)
    keys = "contract_keys:\n" + "".join(f"  - {item}\n" for item in contract_keys) if contract_keys else "contract_keys: []\n"
    (profile / "profile.yaml").write_text(
        profile_yaml + keys + "paper_framework: x/paper-framework.tex\n", encoding="utf-8"
    )
    (profile / "rules.md").write_text(rules, encoding="utf-8")
    for filename, body in (extra_files or {}).items():
        (profile / filename).write_text(body, encoding="utf-8")
    return profile


def block(**values: str) -> str:
    body = "\n".join(f"{key} = {value}" for key, value in values.items())
    return f"# 规则\n\n```toml machine-contract\n{body}\n```\n"


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
            root = core_scaffold(Path(temporary))
            contracts = load_workspace_contracts(root)
            contest_keys = (
                "body_word_minimum",
                "body_page_minimum",
                "body_page_maximum",
                "paper_maximum_bytes",
            )
            for key in contest_keys:
                self.assertFalse(hasattr(contracts, key), key)
            self.assertIn("sandbox", contracts.recommended_project_directories)
            self.assertEqual(contracts.artifact_impact_defaults["results"]["effect"], "STALE")

            merged = vars(load_workspace_contracts(WORKSPACE_ROOT, contest="cumcm"))
            for key in contest_keys:
                self.assertIn(key, merged, key)

    def test_two_profiles_cannot_claim_one_contest(self) -> None:
        with tempfile.TemporaryDirectory(dir=TEMP_ROOT) as temporary:
            root = Path(temporary)
            write_profile(root, "aaa", ("xx",))
            write_profile(root, "bbb", ("xx",))
            with self.assertRaises(ContractError) as caught:
                check_profile_registry(root)
            self.assertIn("claimed by both", str(caught.exception))

    def test_profile_directory_rejects_stray_documents(self) -> None:
        with tempfile.TemporaryDirectory(dir=TEMP_ROOT) as temporary:
            root = Path(temporary)
            write_profile(root, "aaa", ("xx",), extra_files={"notes.md": "# 备忘\n"})
            with self.assertRaises(ContractError) as caught:
                check_profile_registry(root)
            self.assertIn("may contain only", str(caught.exception))

    def test_profile_cannot_redefine_a_core_key(self) -> None:
        with tempfile.TemporaryDirectory(dir=TEMP_ROOT) as temporary:
            root = core_scaffold(Path(temporary))
            write_profile(
                root,
                "aaa",
                ("xx",),
                contract_keys=("body_figure_minimum",),
                rules=block(body_figure_minimum="9"),
            )
            with self.assertRaises(ContractError) as caught:
                load_workspace_contracts(root, contest="xx")
            self.assertIn("cannot redefine Core key", str(caught.exception))

    def test_profile_keys_must_match_the_declaration(self) -> None:
        with tempfile.TemporaryDirectory(dir=TEMP_ROOT) as temporary:
            root = core_scaffold(Path(temporary))
            write_profile(
                root,
                "aaa",
                ("xx",),
                contract_keys=("paper_maximum_bytes",),
                rules=block(archive_maximum_bytes="1"),
            )
            with self.assertRaises(ContractError) as caught:
                load_workspace_contracts(root, contest="xx")
            self.assertIn("do not match profile.yaml contract_keys", str(caught.exception))

    def test_duplicate_key_across_profile_blocks_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory(dir=TEMP_ROOT) as temporary:
            root = core_scaffold(Path(temporary))
            duplicated = block(paper_maximum_bytes="1") + "\n" + block(paper_maximum_bytes="2")
            write_profile(
                root,
                "aaa",
                ("xx",),
                contract_keys=("paper_maximum_bytes",),
                rules=duplicated,
            )
            with self.assertRaises(ContractError) as caught:
                load_workspace_contracts(root, contest="xx")
            self.assertIn("duplicate machine-contract", str(caught.exception))


class CoreBoundaryTests(unittest.TestCase):
    """Core rules and scripts must stay free of any single contest's identity."""

    CONTEST_TERMS = re.compile(r"CUMCM|cumcm|国赛|全国组委会|赛区|支撑材料")

    def core_rule_files(self) -> list[Path]:
        candidates = [
            *sorted((WORKSPACE_ROOT / "docs" / "standards").rglob("*.md")),
            *sorted((WORKSPACE_ROOT / "docs" / "architecture").rglob("*.md")),
            WORKSPACE_ROOT / "docs" / "guides" / "pre-writing-learning.md",
            *sorted((WORKSPACE_ROOT / "tools").glob("*.py")),
            *sorted((WORKSPACE_ROOT / "resources" / "templates").glob("*.md")),
            *sorted((WORKSPACE_ROOT / "resources" / "templates").glob("*.yaml")),
        ]
        for skill in ("modeling-paper-production", "modeling-paper-audit"):
            base = WORKSPACE_ROOT / ".codex" / "skills" / skill
            candidates += sorted(base.rglob("*.md")) + sorted(base.rglob("*.py"))
        return [path for path in candidates if path.is_file()]

    def test_core_rules_name_no_contest(self) -> None:
        leaks = []
        for path in self.core_rule_files():
            text = path.read_text(encoding="utf-8")
            for number, line in enumerate(text.splitlines(), 1):
                if self.CONTEST_TERMS.search(line):
                    leaks.append(f"{path.relative_to(WORKSPACE_ROOT).as_posix()}:{number}")
        self.assertEqual(leaks, [], f"contest-specific facts leaked into Core: {leaks}")


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
            final_audit = project / "07-review" / "final-audit.md"
            self.assertTrue(final_audit.is_file())
            self.assertIn("待填写", final_audit.read_text(encoding="utf-8"))


def latex_paper_source(contracts, figures: int | None = None, tables: int | None = None,
                       narrative_units: int | None = None) -> str:
    """A paper source that satisfies the derived length and visual budgets."""

    figure_count = contracts.body_figure_minimum if figures is None else figures
    table_count = contracts.body_table_minimum if tables is None else tables
    word_minimum = getattr(contracts, "body_word_minimum", 0) or 0
    if narrative_units is None:
        narrative_units = word_minimum // 8 + 50 if word_minimum else 50
    figure_block = "\\begin{figure}\n\\caption{图}\n\\label{fig:q01-%03d}\n\\end{figure}"
    table_block = (
        "\\begin{table}\n\\caption{表}\n\\label{tab:q01-%03d}\n"
        "\\begin{tabular}{cc}\\end{tabular}\n\\end{table}"
    )
    narrative = "结果稳定并且可用，" * narrative_units
    parts = ["\\begin{document}", "\\section{问题重述}", "\\label{page:counted-first}"]
    if word_minimum:
        parts.append("\\label{text:counted-first}")
    parts.append(narrative)
    parts.append("\n".join(figure_block % index for index in range(1, figure_count + 1)))
    parts.append("\n".join(table_block % index for index in range(1, table_count + 1)))
    if word_minimum:
        parts.append("\\label{text:counted-last}")
    parts.extend(
        (
            "\\begin{thebibliography}{99}",
            "\\bibitem{ref-1} 来源一",
            "\\end{thebibliography}",
            "\\label{page:counted-last}",
            "\\appendix",
            "\\section{附录}",
            "\\end{document}",
        )
    )
    return "\n".join(parts)


def write_aux(pages: tuple[int, int]) -> str:
    first, last = pages
    return "\n".join(
        "\\newlabel{%s}{{%d}{%d}{}{}}" % (label, page, page)
        for label, page in (("page:counted-first", first), ("page:counted-last", last))
    )


def write_pdf(path: Path, pages: int) -> None:
    import pymupdf

    document = pymupdf.open()
    for _ in range(pages):
        document.new_page()
    document.save(path)
    document.close()


def build_release_project(project: Path, contracts, contest: str = "cumcm") -> Path:
    """Write a release-candidate project that passes the static preflight.

    Returns the evidence result artifact so a caller can delete it to probe the
    missing-artifact gate. The deliberately wide layout exists because extra
    top-level directories and a low competition score must not block.
    """

    page_minimum = getattr(contracts, "body_page_minimum", 0) or 0
    page_maximum = getattr(contracts, "body_page_maximum", 0) or 30
    counted_last = (1 + page_minimum) if page_minimum else min(page_maximum, 20)
    manifest = getattr(contracts, "delivery_manifest_path", None)
    extra_dirs = list(getattr(contracts, "extra_delivery_directories", ()) or ())

    for relative in (
        "00-admin",
        "01-problem",
        "02-data",
        "03-models",
        "05-evidence",
        "06-paper",
        "07-review",
        "08-delivery",
        "experiments/benchmarks",
        "simulations",
        *extra_dirs,
    ):
        (project / relative).mkdir(parents=True, exist_ok=True)

    (project / "00-admin/project.yaml").write_text(
        f"project_id: fixture\ncontest: {contest}\nyear: 2026\nproblem: a\nstatus: intake\n",
        encoding="utf-8",
    )
    (project / "00-admin/runbook.md").write_text("运行入口已验证。", encoding="utf-8")
    (project / "00-admin/figure-selection-record.md").write_text(
        "# 图片选择记录\n\n图型与载体已按 `PW-FIG-001` 核对。\n", encoding="utf-8"
    )
    (project / "00-admin/pre-writing-learning.md").write_text(
        "learning_status: `COMPLETE`\nstage_record: 写作前学习已由独立审查核对\n", encoding="utf-8"
    )
    (project / "01-problem/problem-checklist.md").write_text("题目与附件已核对。", encoding="utf-8")
    (project / "02-data/data-audit.md").write_text("# 数据审计\n\n四张表已逐列核对。\n", encoding="utf-8")
    (project / "03-models/model-selection.md").write_text(
        "selection_status: `COMPLETE`\nstage_record: 模型选择已由独立审查核对\n", encoding="utf-8"
    )
    result_artifact = project / "experiments" / "benchmarks" / "result.json"
    result_artifact.write_text('{"value": 1}', encoding="utf-8")
    (project / "05-evidence/evidence-index.csv").write_text(
        "claim_id,question_id,claim,evidence_type,source_path,generator,generated_at,status\n"
        "claim-1,part-a,核心结果,metric,experiments/benchmarks/result.json,run.py,2026-09-07T00:00:00,verified\n",
        encoding="utf-8",
    )
    (project / "05-evidence/literature-ledger.csv").write_text(
        "citation_key,title,authors,year,doi_or_url,retrieved_at,used_in,verified\n", encoding="utf-8"
    )
    (project / "05-evidence/ai-tool-log.md").write_text("无未披露的实质使用。", encoding="utf-8")
    (project / "06-paper/main.tex").write_text(latex_paper_source(contracts), encoding="utf-8")
    (project / "06-paper/main.aux").write_text(
        write_aux((2, counted_last)), encoding="utf-8"
    )
    columns = list(contracts.review_log_columns)
    (project / "07-review/review-log.md").write_text(
        "# 审稿台账\n\n| "
        + " | ".join(columns)
        + " |\n|"
        + "|".join("---" for _ in columns)
        + "|\n",
        encoding="utf-8",
    )
    if manifest:
        (project / manifest).write_text("paper.pdf：论文", encoding="utf-8")
    for relative in extra_dirs:
        (project / relative / "q01-solve.py").write_text("print(1)\n", encoding="utf-8")
    pdf = project / "08-delivery/paper.pdf"
    write_pdf(pdf, page_maximum)
    digest = hashlib.sha256(pdf.read_bytes()).hexdigest()
    passes = contracts.final_audit_pass_status
    values = {
        "audit_date": "2026-09-07",
        "audit_phase": contracts.release_candidate_phase_value,
        "review_scope": contracts.release_candidate_review_scopes[0],
        "final_pdf": "08-delivery/paper.pdf",
        "final_pdf_sha256": digest,
        "official_rules_gate": passes,
        "evidence_gate": passes,
        "clean_reproduction_gate": contracts.release_candidate_reproduction_statuses[0],
        "anonymity_gate": passes,
        "delivery_gate": passes,
        "open_critical": contracts.final_audit_no_open_findings_value,
        "open_major": contracts.final_audit_no_open_findings_value,
        "release_decision": contracts.release_ready_status,
    }
    (project / "07-review/final-audit.md").write_text(
        "\n".join(
            (
                "# 最终审查报告",
                "",
                "## 机器可读摘要",
                "",
                *(f"- {name}: `{values[name]}`" for name in contracts.final_audit_fields),
                "",
                "## 竞争力评分",
                "- total_score: 40",
                "- grade: D",
            )
        ),
        encoding="utf-8",
    )
    return result_artifact


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
            result_artifact = build_release_project(project, contracts)

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


class GateIntegrityTests(unittest.TestCase):
    """Each gate below must reject a concrete bypass that used to pass."""

    def setUp(self) -> None:
        self.contracts = load_workspace_contracts(WORKSPACE_ROOT, contest="cumcm")

    def audit(self, project: Path, phase: str = "release-candidate"):
        return run(str(AUDIT_SCRIPT), str(project), "--phase", phase)

    def project_in(self, case: str) -> Path:
        temporary = tempfile.mkdtemp(dir=TEMP_ROOT)
        self.addCleanup(shutil.rmtree, temporary, True)
        project = Path(temporary) / case
        build_release_project(project, self.contracts)
        return project

    def test_repeated_final_audit_fields_are_rejected(self) -> None:
        project = self.project_in("repeated-fields")
        report = project / "07-review/final-audit.md"
        original = report.read_text(encoding="utf-8")
        blocked = original.replace(
            f"- release_decision: `{self.contracts.release_ready_status}`",
            "- release_decision: `BLOCKED`",
            1,
        )
        self.assertNotEqual(blocked, original)
        report.write_text(blocked, encoding="utf-8")
        self.assertNotEqual(self.audit(project).returncode, 0)

        appended = blocked.replace(
            "- release_decision: `BLOCKED`",
            f"- release_decision: `BLOCKED`\n- release_decision: `{self.contracts.release_ready_status}`",
            1,
        )
        report.write_text(appended, encoding="utf-8")
        rejected = self.audit(project)
        self.assertNotEqual(rejected.returncode, 0)
        self.assertIn("repeats fields", rejected.stdout)

    def test_field_order_must_follow_the_contract(self) -> None:
        project = self.project_in("field-order")
        report = project / "07-review/final-audit.md"
        lines = report.read_text(encoding="utf-8").splitlines()
        summary_at = lines.index("## 机器可读摘要")
        fields = [
            index
            for index, line in enumerate(lines)
            if index > summary_at and line.startswith("- ")
        ]
        lines[fields[0]], lines[fields[1]] = lines[fields[1]], lines[fields[0]]
        report.write_text("\n".join(lines), encoding="utf-8")
        blocked = self.audit(project)
        self.assertNotEqual(blocked.returncode, 0)
        self.assertIn("contract order", blocked.stdout)

    def test_derived_counts_catch_a_thin_paper(self) -> None:
        project = self.project_in("thin-paper")
        (project / "06-paper/main.tex").write_text(
            latex_paper_source(self.contracts, figures=2, tables=1, narrative_units=10),
            encoding="utf-8",
        )
        blocked = self.audit(project)
        self.assertNotEqual(blocked.returncode, 0)
        self.assertIn("narrative length", blocked.stdout)
        self.assertIn("counted figures", blocked.stdout)
        self.assertIn("counted tables", blocked.stdout)

    def test_missing_region_label_is_reported(self) -> None:
        project = self.project_in("no-label")
        source = (project / "06-paper/main.tex").read_text(encoding="utf-8")
        (project / "06-paper/main.tex").write_text(
            source.replace("\\label{page:counted-last}\n", ""), encoding="utf-8"
        )
        self.assertIn("cannot delimit the counted region", self.audit(project).stdout)

    def test_missing_text_region_label_is_reported(self) -> None:
        project = self.project_in("no-text-label")
        source = (project / "06-paper/main.tex").read_text(encoding="utf-8")
        (project / "06-paper/main.tex").write_text(
            source.replace("\\label{text:counted-last}\n", ""), encoding="utf-8"
        )
        blocked = self.audit(project)
        self.assertIn("cannot delimit the counted region", blocked.stdout)
        self.assertIn("text:counted-last", blocked.stdout)

    def test_missing_aux_file_is_reported(self) -> None:
        project = self.project_in("no-aux")
        (project / "06-paper/main.aux").unlink()
        self.assertIn("main.aux is missing", self.audit(project).stdout)

    def test_non_pdf_bytes_cannot_pass_page_check(self) -> None:
        project = self.project_in("fake-pdf")
        pdf = project / "08-delivery" / "paper.pdf"
        pdf.write_bytes(b"%PDF-1.4 this is not a PDF")
        digest = hashlib.sha256(pdf.read_bytes()).hexdigest()
        report = project / "07-review" / "final-audit.md"
        report.write_text(
            re.sub(
                r"- final_pdf_sha256: `[0-9a-f]+`",
                f"- final_pdf_sha256: `{digest}`",
                report.read_text(encoding="utf-8"),
            ),
            encoding="utf-8",
        )
        self.assertIn("cannot be opened for page counting", self.audit(project).stdout)

    def test_page_maximum_is_enforced_from_the_aux_labels(self) -> None:
        project = self.project_in("too-many-pages")
        oversized = 1 + self.contracts.body_page_maximum + 5
        (project / "06-paper" / "main.aux").write_text(
            write_aux((2, oversized)), encoding="utf-8"
        )
        blocked = self.audit(project)
        self.assertIn("exceeds body_page_maximum", blocked.stdout)

    def test_draft_evidence_blocks_only_at_final(self) -> None:
        project = self.project_in("draft-evidence")
        index = project / "05-evidence/evidence-index.csv"
        index.write_text(
            index.read_text(encoding="utf-8").replace(",verified\n", ",draft\n"),
            encoding="utf-8",
        )
        self.assertEqual(self.audit(project).returncode, 0)
        final = self.audit(project, "final")
        self.assertNotEqual(final.returncode, 0)
        self.assertIn("must be 'verified' at the final phase", final.stdout)

    def test_profile_delivery_directory_must_hold_content(self) -> None:
        project = self.project_in("empty-support")
        shutil.rmtree(project / "08-delivery" / "support-materials")
        missing = self.audit(project)
        self.assertNotEqual(missing.returncode, 0)
        self.assertIn("missing profile-declared delivery directory", missing.stdout)

        (project / "08-delivery" / "support-materials").mkdir()
        empty = self.audit(project)
        self.assertNotEqual(empty.returncode, 0)
        self.assertIn("delivery directory is empty", empty.stdout)

    def test_review_ledger_must_match_open_counts(self) -> None:
        project = self.project_in("ledger-disagreement")
        columns = list(self.contracts.review_log_columns)
        row = ["F-1", "CRITICAL", "06-paper/main.tex", "PW-LEN-001", "结论无数据", "无", "补齐", "未核", "OPEN"]
        self.assertEqual(len(row), len(columns))
        (project / "07-review/review-log.md").write_text(
            "# 审稿台账\n\n| "
            + " | ".join(columns)
            + " |\n|"
            + "|".join("---" for _ in columns)
            + "|\n| "
            + " | ".join(row)
            + " |\n",
            encoding="utf-8",
        )
        blocked = self.audit(project)
        self.assertNotEqual(blocked.returncode, 0)
        self.assertIn("review ledger records 1 open CRITICAL findings", blocked.stdout)

    def test_unfilled_workspace_record_blocks_release(self) -> None:
        project = self.project_in("unfilled-record")
        (project / "00-admin/figure-selection-record.md").write_text(
            "# 图片选择记录\n\n| figure_label | 状态 |\n|---|---|\n| fig:q01-001 | 待填写 |\n",
            encoding="utf-8",
        )
        blocked = self.audit(project)
        self.assertNotEqual(blocked.returncode, 0)
        self.assertIn("unresolved placeholder in 00-admin/figure-selection-record.md", blocked.stdout)

    def test_declared_profile_must_match_contest(self) -> None:
        project = self.project_in("profile-mismatch")
        (project / "00-admin/project.yaml").write_text(
            "project_id: fixture\ncontest: mcm\nprofile: cumcm\nyear: 2027\nproblem: a\nstatus: intake\n",
            encoding="utf-8",
        )
        blocked = self.audit(project)
        self.assertNotEqual(blocked.returncode, 0)
        self.assertIn("resolves to 'mcm-icm'", blocked.stdout)
        self.assertIn("Audit profile: mcm-icm", blocked.stdout)

    def test_profile_directory_name_is_not_a_contest(self) -> None:
        with tempfile.TemporaryDirectory(dir=TEMP_ROOT) as temporary:
            result = run(
                str(INIT_SCRIPT),
                "--root",
                temporary,
                "--contest",
                "mcm-icm",
                "--year",
                "2027",
                "--problem",
                "a",
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("unknown contest", (result.stdout + result.stderr).lower())


class ProfileGateTests(unittest.TestCase):
    """Declared floors bite; absent floors stay silent. Same code path per profile."""

    def build(self, temporary: str, contest: str, **paper_kwargs) -> Path:
        contracts = load_workspace_contracts(WORKSPACE_ROOT, contest=contest)
        project = Path(temporary) / f"{contest}-project"
        build_release_project(project, contracts, contest)
        if paper_kwargs:
            (project / "06-paper/main.tex").write_text(
                latex_paper_source(contracts, **paper_kwargs), encoding="utf-8"
            )
        return project

    def test_compliant_project_passes_for_every_declared_contest(self) -> None:
        for contest in ("cumcm", "mcm", "icm"):
            with self.subTest(contest=contest), tempfile.TemporaryDirectory(dir=TEMP_ROOT) as temporary:
                project = self.build(temporary, contest)
                result = run(str(AUDIT_SCRIPT), str(project), "--phase", "release-candidate")
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_page_floor_only_applies_where_the_profile_declares_it(self) -> None:
        for contest, blocked in (("cumcm", True), ("mcm", False)):
            with self.subTest(contest=contest), tempfile.TemporaryDirectory(dir=TEMP_ROOT) as temporary:
                project = self.build(temporary, contest)
                (project / "06-paper/main.aux").write_text(write_aux((2, 7)), encoding="utf-8")
                result = run(str(AUDIT_SCRIPT), str(project), "--phase", "release-candidate")
                if blocked:
                    self.assertNotEqual(result.returncode, 0)
                    self.assertIn("below body_page_minimum", result.stdout)
                else:
                    self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_word_floor_only_applies_where_the_profile_declares_it(self) -> None:
        for contest, blocked in (("cumcm", True), ("mcm", False)):
            with self.subTest(contest=contest), tempfile.TemporaryDirectory(dir=TEMP_ROOT) as temporary:
                project = self.build(temporary, contest, narrative_units=5)
                result = run(str(AUDIT_SCRIPT), str(project), "--phase", "release-candidate")
                if blocked:
                    self.assertNotEqual(result.returncode, 0)
                    self.assertIn("narrative length", result.stdout)
                else:
                    self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_visual_floor_is_shared_across_contests(self) -> None:
        for contest in ("cumcm", "mcm"):
            with self.subTest(contest=contest), tempfile.TemporaryDirectory(dir=TEMP_ROOT) as temporary:
                project = self.build(temporary, contest, figures=1, tables=1)
                result = run(str(AUDIT_SCRIPT), str(project), "--phase", "release-candidate")
                self.assertNotEqual(result.returncode, 0)
                self.assertIn("counted figures", result.stdout)
                self.assertIn("counted tables", result.stdout)

    def test_icm_project_initializes_and_audits(self) -> None:
        with tempfile.TemporaryDirectory(dir=TEMP_ROOT) as temporary:
            created = run(
                str(INIT_SCRIPT),
                "--root",
                temporary,
                "--contest",
                "icm",
                "--year",
                "2027",
                "--problem",
                "f",
            )
            self.assertEqual(created.returncode, 0, created.stdout + created.stderr)
            project = Path(temporary) / "icm-2027-f"
            self.assertTrue((project / "07-review/final-audit.md").is_file())
            self.assertFalse((project / "08-delivery/support-materials").exists())
            draft = run(str(AUDIT_SCRIPT), str(project), "--phase", "draft")
            self.assertEqual(draft.returncode, 0, draft.stdout + draft.stderr)
            self.assertIn("Audit profile: mcm-icm", draft.stdout)


class FrameworkTests(unittest.TestCase):
    """The two paper frameworks are the implementation of the profiles' shapes."""

    NON_PADDED_QUESTION = re.compile(r"(?<![\d:])q[1-9](?![\d])")
    LITERAL_PLACEHOLDER = re.compile(r"\\textbf\{【|\\textbf\{\[")

    def framework(self, profile: str) -> str:
        path = WORKSPACE_ROOT / "resources" / "templates" / "contests" / profile / "paper-framework.tex"
        return path.read_text(encoding="utf-8")

    def test_paths_and_labels_use_padded_question_numbers(self) -> None:
        for profile in ("cumcm", "mcm-icm"):
            with self.subTest(profile=profile):
                found = self.NON_PADDED_QUESTION.findall(self.framework(profile))
                self.assertEqual(found, [], f"{profile}: non-padded question tokens {found[:5]}")

    def test_frameworks_reach_the_shared_visual_floor(self) -> None:
        contracts = load_workspace_contracts(WORKSPACE_ROOT, contest="mcm")
        for profile in ("cumcm", "mcm-icm"):
            with self.subTest(profile=profile):
                text = self.framework(profile)
                self.assertGreaterEqual(
                    len(re.findall(r"\\begin\{figure\}", text)), contracts.body_figure_minimum
                )
                self.assertGreaterEqual(
                    len(re.findall(r"\\begin\{table\}", text)), contracts.body_table_minimum
                )

    def test_frameworks_declare_their_counted_regions(self) -> None:
        for profile, labels in (
            ("cumcm", ("page:counted-first", "page:counted-last", "text:counted-first", "text:counted-last")),
            ("mcm-icm", ("page:counted-first", "page:counted-last")),
        ):
            with self.subTest(profile=profile):
                text = self.framework(profile)
                for label in labels:
                    self.assertIn(f"\\label{{{label}}}", text, label)

    def test_only_the_macro_definition_may_render_literal_brackets(self) -> None:
        for profile in ("cumcm", "mcm-icm"):
            with self.subTest(profile=profile):
                lines = [
                    line
                    for line in self.framework(profile).splitlines()
                    if self.LITERAL_PLACEHOLDER.search(line)
                ]
                self.assertEqual(
                    [line for line in lines if "\\newcommand{\\TemplateField}" not in line],
                    [],
                    "unfilled slots must use \\TemplateField so the auditor can see them",
                )

    def test_text_region_ends_before_the_bibliography(self) -> None:
        text = self.framework("cumcm")
        self.assertLess(
            text.index("\\label{text:counted-last}"),
            text.index("\\begin{thebibliography}"),
            "the narrative word region must exclude the reference list",
        )
        self.assertLess(
            text.index("\\label{text:counted-last}"), text.index("\\label{page:counted-last}")
        )


if __name__ == "__main__":
    unittest.main()
