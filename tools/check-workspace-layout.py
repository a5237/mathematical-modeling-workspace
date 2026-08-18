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
    "config/python/requirements-modeling.txt",
    "docs/architecture/workspace-layout.md",
    "docs/guides/modeling-environment.md",
    "docs/standards/naming.md",
    "docs/standards/paper-writing.md",
    "docs/standards/workspace-governance.md",
    "resources/paper-library",
    "resources/templates",
    "tools/check-modeling-env.py",
    "var/tmp/README.md",
    "workspace/archive",
    "workspace/inbox",
    "workspace/projects",
)

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
    print("  OK   deprecated root paths absent")
    print("  OK   project and inbox directory names")
    print("\nRESULT: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
