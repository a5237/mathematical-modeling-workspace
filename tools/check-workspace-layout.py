#!/usr/bin/env python3
"""Validate the repository-level workspace layout without modifying files."""

from __future__ import annotations

import re
from pathlib import Path


WORKSPACE_ROOT = Path(__file__).resolve().parent.parent

ALLOWED_ROOT_FILES = {
    ".gitignore",
    "AGENTS.md",
    "README.md",
}
ALLOWED_ROOT_DIRS = {
    ".agents",
    ".codex",
    ".git",
    ".venv-modeling",
    "config",
    "docs",
    "resources",
    "tools",
    "var",
    "workspace",
}

REQUIRED_PATHS = (
    ".codex/skills/cumcm-paper-audit/SKILL.md",
    ".codex/skills/cumcm-paper-production/SKILL.md",
    "config/python/requirements-modeling.txt",
    "docs/architecture/workspace-layout.md",
    "docs/guides/modeling-environment.md",
    "docs/guides/pre-writing-learning.md",
    "docs/standards/cumcm-current-rules.md",
    "docs/standards/evidence-contract.md",
    "docs/standards/naming.md",
    "docs/standards/paper-figures.md",
    "docs/standards/paper-quality-audit.md",
    "docs/standards/paper-writing.md",
    "docs/standards/workspace-governance.md",
    "resources/paper-library",
    "resources/algorithm-library/README.md",
    "resources/algorithm-library/index.md",
    "resources/algorithm-library/01-优化算法说明.md",
    "resources/algorithm-library/02-预测类算法说明.md",
    "resources/algorithm-library/03-评价类算法说明.md",
    "resources/algorithm-library/04-图论与网络分析算法说明.md",
    "resources/algorithm-library/05-统计分析与数据处理算法说明.md",
    "resources/algorithm-library/06-综合类算法说明.md",
    "resources/algorithm-library/07-机器学习算法说明.md",
    "resources/templates",
    "resources/templates/figure-selection-record.md",
    "tools/check-modeling-env.py",
    "var/tmp/README.md",
    "workspace/archive",
    "workspace/inbox",
    "workspace/projects",
)

AGENT_PATH_POLICY_MARKERS = {
    "AGENTS.md": "Agent 工具路径约定",
    ".codex/skills/cumcm-paper-production/SKILL.md": "follow the resolution convention in `AGENTS.md`",
    ".codex/skills/cumcm-paper-audit/SKILL.md": "follow the resolution convention in `AGENTS.md`",
}

DEPRECATED_ROOT_PATHS = (
    "00-inbox",
    "archive",
    "paper-library",
    "paper-system",
    "projects",
    "requirements-modeling.txt",
    "shared-tools",
    "templates",
    "tmp",
    "数学建模工作区_Agent强制规范.md",
    "数学建模论文写作_Agent强制规范.md",
    "数模环境说明.md",
)

PROJECT_NAME = re.compile(r"^[a-z0-9-]+-\d{4}-[a-z0-9-]+$")
INBOX_NAME = re.compile(r"^\d{4}-\d{2}-\d{2}-[a-z0-9-]+$")


def visible_directories(parent: Path) -> list[Path]:
    return sorted(path for path in parent.iterdir() if path.is_dir())


def main() -> int:
    errors: list[str] = []

    for entry in WORKSPACE_ROOT.iterdir():
        allowed = entry.name in (ALLOWED_ROOT_DIRS if entry.is_dir() else ALLOWED_ROOT_FILES)
        if not allowed:
            errors.append(f"unexpected root entry: {entry.name}")

    for relative in REQUIRED_PATHS:
        if not (WORKSPACE_ROOT / relative).exists():
            errors.append(f"missing required path: {relative}")

    for relative, marker in AGENT_PATH_POLICY_MARKERS.items():
        path = WORKSPACE_ROOT / relative
        if path.is_file() and marker not in path.read_text(encoding="utf-8"):
            errors.append(f"missing Agent path-policy reference: {relative}")

    for relative in DEPRECATED_ROOT_PATHS:
        if (WORKSPACE_ROOT / relative).exists():
            errors.append(f"deprecated root path returned: {relative}")

    projects = WORKSPACE_ROOT / "workspace" / "projects"
    if projects.is_dir():
        for project in visible_directories(projects):
            if not PROJECT_NAME.fullmatch(project.name):
                errors.append(f"invalid project directory name: workspace/projects/{project.name}")

    inbox = WORKSPACE_ROOT / "workspace" / "inbox"
    if inbox.is_dir():
        for request in visible_directories(inbox):
            if not INBOX_NAME.fullmatch(request.name):
                errors.append(f"invalid inbox directory name: workspace/inbox/{request.name}")

    if errors:
        print("[Workspace layout]")
        for error in errors:
            print(f"  FAIL {error}")
        print("\nRESULT: FAIL")
        return 1

    print("[Workspace layout]")
    print("  OK   root allowlist")
    print("  OK   required layers and entry files")
    print("  OK   Agent path-policy references")
    print("  OK   deprecated root paths absent")
    print("  OK   project and inbox directory names")
    print("\nRESULT: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
