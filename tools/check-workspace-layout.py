#!/usr/bin/env python3
"""Detect high-risk pollution without freezing the repository layout."""

from __future__ import annotations

import argparse
from pathlib import Path


WORKSPACE_ROOT = Path(__file__).resolve().parent.parent

# Unknown new roots are intentionally allowed. Only paths that recreate an
# obsolete, competing authority root are blocked.
CONFLICTING_DEPRECATED_PATHS = (
    "00-inbox",
    "archive",
    "paper-library",
    "paper-system",
    "projects",
    "requirements-modeling.txt",
    "shared-tools",
    "templates",
    "tmp",
)

DEPRECATED_ROOT_DOCUMENTS = (
    "数学建模工作区_Agent强制规范.md",
    "数学建模论文写作_Agent强制规范.md",
    "数模环境说明.md",
)

RUNTIME_DIRECTORY_NAMES = {
    "__pycache__",
    ".ipynb_checkpoints",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    ".mplconfig",
    "build",
    "dist",
}

GENERATED_SUFFIXES = (
    ".aux",
    ".fdb_latexmk",
    ".fls",
    ".out",
    ".pyc",
    ".synctex.gz",
    ".tmp",
    ".toc",
    ".xdv",
)

PROJECT_ARTIFACT_SUFFIXES = {
    ".csv",
    ".docx",
    ".feather",
    ".h5",
    ".hdf5",
    ".mat",
    ".npy",
    ".npz",
    ".parquet",
    ".pdf",
    ".pickle",
    ".pkl",
    ".sav",
    ".svg",
    ".tex",
    ".tif",
    ".tiff",
    ".tsv",
    ".xls",
    ".xlsm",
    ".xlsx",
    ".jpg",
    ".jpeg",
    ".png",
}

PROJECT_SOURCE_SUFFIXES = {".ipynb", ".jl", ".m", ".py", ".r"}
PROJECT_ARTIFACT_BURST = 5
PROJECT_SOURCE_BURST = 3


def is_generated_file(path: Path) -> bool:
    name = path.name.lower()
    return name.startswith("~$") or any(name.endswith(suffix) for suffix in GENERATED_SUFFIXES)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=WORKSPACE_ROOT)
    args = parser.parse_args()
    root = args.root.resolve()
    if not root.is_dir():
        parser.error(f"workspace root does not exist: {root}")

    failures: list[str] = []
    warnings: list[str] = []

    for relative in CONFLICTING_DEPRECATED_PATHS:
        if (root / relative).exists():
            failures.append(f"conflicting deprecated root path: {relative}")

    for relative in DEPRECATED_ROOT_DOCUMENTS:
        if (root / relative).exists():
            warnings.append(f"deprecated root document should be routed under docs/: {relative}")

    entries = list(root.iterdir())
    for entry in entries:
        lowered = entry.name.lower()
        if entry.is_dir() and (lowered in RUNTIME_DIRECTORY_NAMES or lowered.startswith("_minted-")):
            failures.append(f"runtime/cache directory at workspace root: {entry.name}")
        elif entry.is_file() and is_generated_file(entry):
            failures.append(f"generated or temporary file at workspace root: {entry.name}")

    root_files = [entry for entry in entries if entry.is_file()]
    artifact_files = [entry for entry in root_files if entry.suffix.lower() in PROJECT_ARTIFACT_SUFFIXES]
    source_files = [entry for entry in root_files if entry.suffix.lower() in PROJECT_SOURCE_SUFFIXES]

    if len(artifact_files) >= PROJECT_ARTIFACT_BURST:
        failures.append(
            f"project-artifact burst at workspace root ({len(artifact_files)} files; route into a project)"
        )
    elif artifact_files:
        warnings.append(
            "possible project data/result at workspace root: "
            + ", ".join(path.name for path in sorted(artifact_files))
        )

    if len(source_files) >= PROJECT_SOURCE_BURST:
        failures.append(
            f"project-source burst at workspace root ({len(source_files)} files; route into tools/ or a project)"
        )
    elif source_files:
        warnings.append(
            "source file at workspace root; confirm it is a repository entry point: "
            + ", ".join(path.name for path in sorted(source_files))
        )

    print(f"Workspace root: {root}")
    print("[High-risk workspace hygiene]")
    for item in warnings:
        print(f"  WARN {item}")
    for item in failures:
        print(f"  FAIL {item}")

    if failures:
        print("\nRESULT: FAIL")
        return 1
    print("  OK   no high-risk root pollution detected" if not warnings else "  OK   no blocking issue detected")
    print("\nRESULT: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
