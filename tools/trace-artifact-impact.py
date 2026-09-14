#!/usr/bin/env python3
"""Trace downstream impact from changed project artifacts without writing state."""

from __future__ import annotations

import argparse
from collections import defaultdict, deque
import json
from pathlib import Path, PurePosixPath
import re
from typing import Any, Iterable

try:
    import yaml
except ImportError as exc:  # pragma: no cover - exercised only outside the workspace environment
    raise SystemExit(
        "PyYAML is required; run this tool with .venv-modeling/Scripts/python.exe"
    ) from exc


MAP_RELATIVE_PATH = Path("00-admin/artifact-map.yaml")
DEFAULT_MAP_TEMPLATE = (
    Path(__file__).resolve().parents[1] / "resources" / "templates" / "artifact-map.yaml"
)
PATH_CATEGORIES = (
    "data",
    "code",
    "parameters",
    "results",
    "validation",
    "paper_assets",
)
ALL_CATEGORIES = PATH_CATEGORIES + ("evidence", "paper", "review", "delivery")
SEMANTIC_CATEGORIES = {"evidence", "paper", "review", "delivery"}
INDEX_CATEGORIES = {
    "claims": "evidence",
    "literature": "evidence",
    "paper": "paper",
    "review": "review",
    "delivery": "delivery",
}
QUESTION_REFERENCE = re.compile(r"^(q\d+)\.([a-z_]+)$", re.IGNORECASE)
QUESTION_TOKEN = re.compile(r"(?<![a-z0-9])q\d+(?![a-z0-9])", re.IGNORECASE)
STATUS_RANK = {"RECHECK": 1, "STALE": 2, "CHANGED": 3}

Node = tuple[str, str]


class ImpactMapError(ValueError):
    """Raised when the artifact map cannot be interpreted safely."""


def within(path: Path, root: Path) -> bool:
    try:
        path.relative_to(root)
        return True
    except ValueError:
        return False


def normalize_map_path(value: Any, label: str, warnings: list[str]) -> str | None:
    if not isinstance(value, str) or not value.strip():
        warnings.append(f"ignored non-string or empty path at {label}")
        return None
    text = value.strip().replace("\\", "/")
    if re.match(r"^[a-zA-Z]:", text):
        warnings.append(f"ignored absolute path at {label}: {value}")
        return None
    pure = PurePosixPath(text)
    if pure.is_absolute() or ".." in pure.parts:
        warnings.append(f"ignored unsafe path at {label}: {value}")
        return None
    normalized = "/".join(part for part in pure.parts if part not in ("", "."))
    if not normalized:
        warnings.append(f"ignored empty normalized path at {label}")
        return None
    return normalized


def normalize_changed_path(value: str, project: Path) -> str:
    raw = Path(value)
    if raw.is_absolute():
        candidate = raw.resolve(strict=False)
    else:
        cwd_candidate = (Path.cwd() / raw).resolve(strict=False)
        candidate = cwd_candidate if within(cwd_candidate, project) else (project / raw).resolve(strict=False)
    if not within(candidate, project):
        raise ImpactMapError(f"changed path escapes the project root: {value}")
    return candidate.relative_to(project).as_posix()


def load_artifact_map(project: Path) -> tuple[dict[str, Any], list[str], bool]:
    path = project / MAP_RELATIVE_PATH
    if not path.is_file():
        return {}, [f"artifact map is missing; using path-prefix inference: {MAP_RELATIVE_PATH.as_posix()}"], False
    try:
        loaded = yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, yaml.YAMLError) as exc:
        raise ImpactMapError(f"cannot read artifact map: {exc}") from exc
    if loaded is None:
        loaded = {}
    if not isinstance(loaded, dict):
        raise ImpactMapError("artifact map root must be a mapping")
    return loaded, [], True


def mapping(value: Any, label: str) -> dict[str, Any]:
    if value is None:
        return {}
    if not isinstance(value, dict):
        raise ImpactMapError(f"{label} must be a mapping")
    return value


def sequence(value: Any, label: str) -> list[Any]:
    if value is None:
        return []
    if not isinstance(value, list):
        raise ImpactMapError(f"{label} must be a list")
    return value


def parse_impact_defaults(raw: Any, warnings: list[str]) -> dict[str, dict[str, Any]]:
    if raw is None:
        try:
            template = yaml.safe_load(DEFAULT_MAP_TEMPLATE.read_text(encoding="utf-8"))
        except (OSError, UnicodeError, yaml.YAMLError) as exc:
            raise ImpactMapError(f"cannot load default impact graph: {exc}") from exc
        if not isinstance(template, dict) or "impact_defaults" not in template:
            raise ImpactMapError("default artifact-map template has no impact_defaults")
        raw = template["impact_defaults"]
        warnings.append(
            "impact_defaults is missing; using the workspace artifact-map template"
        )
    specs = mapping(raw, "impact_defaults")
    if not specs:
        raise ImpactMapError("impact_defaults cannot be empty")
    parsed: dict[str, dict[str, Any]] = {}
    for target, raw_spec in specs.items():
        if target not in ALL_CATEGORIES:
            raise ImpactMapError(f"impact_defaults has unknown target category: {target}")
        spec = mapping(raw_spec, f"impact_defaults.{target}")
        dependencies = sequence(spec.get("depends_on"), f"impact_defaults.{target}.depends_on")
        if not dependencies or any(item not in ALL_CATEGORIES for item in dependencies):
            raise ImpactMapError(
                f"impact_defaults.{target}.depends_on must contain known categories"
            )
        effect = str(spec.get("effect", "")).upper()
        if effect not in {"STALE", "RECHECK"}:
            raise ImpactMapError(f"impact_defaults.{target}.effect must be STALE or RECHECK")
        parsed[target] = {"depends_on": dependencies, "effect": effect}
    return parsed


def extract_question_id(relative_path: str) -> str | None:
    match = QUESTION_TOKEN.search(relative_path.lower())
    return match.group(0).lower() if match else None


def infer_category(relative_path: str) -> tuple[str | None, str | None]:
    lower = relative_path.lower()
    parts = PurePosixPath(lower).parts
    if not parts:
        return None, None
    if parts[0] == "01-problem":
        return "data", "problem change was conservatively treated as an upstream data change"
    if parts[0] == "02-data":
        return "data", None
    if parts[0] == "03-models":
        filename = parts[-1]
        parameter_like = (
            "parameter" in filename
            or "config" in filename
            or PurePosixPath(filename).suffix in {".yaml", ".yml", ".toml"}
        )
        return ("parameters" if parameter_like else "code"), None
    if parts[0] == "04-results":
        validation_tokens = (
            "valid",
            "check",
            "sensitivity",
            "robust",
            "residual",
            "convergence",
            "ablation",
            "benchmark",
        )
        if any(token in lower for token in validation_tokens):
            return "validation", None
        return "results", None
    if parts[0] == "05-evidence":
        return "evidence", None
    if parts[0] == "06-paper":
        if len(parts) > 1 and parts[1] in {"figures", "tables"}:
            return "paper_assets", None
        return "paper", None
    if parts[0] == "07-review":
        return "review", None
    if parts[0] == "08-delivery":
        return "delivery", None
    if lower == "00-admin/project.yaml":
        return "parameters", "project metadata change was conservatively treated as parameters"
    return None, None


def add_registered_paths(
    registry: dict[str, list[Node]],
    owner: str,
    values: Any,
    category: str,
    label: str,
    warnings: list[str],
) -> None:
    for index, raw_path in enumerate(sequence(values, label), start=1):
        normalized = normalize_map_path(raw_path, f"{label}[{index}]", warnings)
        if normalized:
            registry[normalized.casefold()].append((owner, category))


def build_registry(
    artifact_map: dict[str, Any], warnings: list[str]
) -> tuple[dict[str, list[Node]], dict[str, Any], dict[str, Any], dict[str, Any]]:
    registry: dict[str, list[Node]] = defaultdict(list)
    common = mapping(artifact_map.get("common"), "common")
    raw_questions = mapping(artifact_map.get("questions"), "questions")
    questions: dict[str, Any] = {}
    indexes = mapping(artifact_map.get("indexes"), "indexes")

    for category in PATH_CATEGORIES:
        add_registered_paths(
            registry, "common", common.get(category), category, f"common.{category}", warnings
        )
    for raw_question_id, raw_question in raw_questions.items():
        question_id = str(raw_question_id).lower()
        question = mapping(raw_question, f"questions.{raw_question_id}")
        if question_id in questions:
            raise ImpactMapError(f"duplicate question_id after normalization: {question_id}")
        questions[question_id] = question
        for category in PATH_CATEGORIES:
            add_registered_paths(
                registry,
                question_id,
                question.get(category),
                category,
                f"questions.{raw_question_id}.{category}",
                warnings,
            )
    for index_name, category in INDEX_CATEGORIES.items():
        if index_name not in indexes:
            continue
        normalized = normalize_map_path(
            indexes.get(index_name), f"indexes.{index_name}", warnings
        )
        if normalized:
            registry[normalized.casefold()].append(("*", category))
    return registry, common, questions, indexes


def seed_for_owner(owner: str, category: str, question_ids: Iterable[str]) -> list[Node]:
    if owner == "common":
        return [("common", category), *((question_id, category) for question_id in question_ids)]
    if owner == "*":
        scopes = list(question_ids) or ["project"]
        return [(scope, category) for scope in scopes]
    return [(owner, category)]


def classify_changes(
    changed_paths: list[str],
    registry: dict[str, list[Node]],
    initial_question_ids: list[str],
    warnings: list[str],
) -> tuple[dict[Node, set[str]], list[dict[str, str]], set[str], set[str]]:
    seeds: dict[Node, set[str]] = defaultdict(set)
    matches: list[dict[str, str]] = []
    question_ids = set(initial_question_ids)
    sources: set[str] = set()

    for relative_path in changed_paths:
        registered = registry.get(relative_path.casefold(), [])
        if registered:
            sources.add("artifact-map")
            for owner, category in registered:
                for node in seed_for_owner(owner, category, sorted(question_ids)):
                    seeds[node].add(relative_path)
                matches.append(
                    {
                        "path": relative_path,
                        "scope": "all questions" if owner == "*" else owner,
                        "category": category,
                        "source": "artifact-map",
                    }
                )
            continue

        category, note = infer_category(relative_path)
        if category is None:
            warnings.append(f"could not classify changed path; inspect it manually: {relative_path}")
            continue
        sources.add("path-prefix")
        if note:
            warnings.append(f"{relative_path}: {note}")
        question_id = extract_question_id(relative_path)
        if question_id:
            question_ids.add(question_id)
            scopes = [question_id]
        elif question_ids:
            scopes = sorted(question_ids)
            warnings.append(
                f"{relative_path}: no question_id was found, so all mapped questions were included"
            )
        else:
            scopes = ["project"]
        for scope in scopes:
            seeds[(scope, category)].add(relative_path)
            matches.append(
                {
                    "path": relative_path,
                    "scope": scope,
                    "category": category,
                    "source": "path-prefix",
                }
            )
    question_ids.update(scope for scope, _category in seeds if scope != "common")
    return seeds, matches, question_ids, sources


def build_edges(
    scopes: Iterable[str],
    defaults: dict[str, dict[str, Any]],
    questions: dict[str, Any],
) -> dict[Node, list[tuple[Node, str]]]:
    edges: dict[Node, list[tuple[Node, str]]] = defaultdict(list)
    all_scopes = set(scopes)
    all_scopes.add("common")

    cross_edges: list[tuple[Node, Node]] = []
    for raw_question_id, raw_question in questions.items():
        question_id = str(raw_question_id).lower()
        question = mapping(raw_question, f"questions.{raw_question_id}")
        references = sequence(
            question.get("depends_on_questions"),
            f"questions.{raw_question_id}.depends_on_questions",
        )
        for raw_reference in references:
            if not isinstance(raw_reference, str):
                raise ImpactMapError(
                    f"questions.{raw_question_id}.depends_on_questions must contain strings"
                )
            match = QUESTION_REFERENCE.fullmatch(raw_reference.strip())
            if not match or match.group(2).lower() not in ALL_CATEGORIES:
                raise ImpactMapError(
                    f"invalid cross-question dependency {raw_reference!r}; use qNN.category"
                )
            source = (match.group(1).lower(), match.group(2).lower())
            target = (question_id, "results")
            all_scopes.update((source[0], question_id))
            cross_edges.append((source, target))

    for scope in sorted(all_scopes):
        for target_category, spec in defaults.items():
            if scope == "common" and target_category in SEMANTIC_CATEGORIES:
                continue
            for dependency in spec["depends_on"]:
                edges[(scope, dependency)].append(
                    ((scope, target_category), spec["effect"])
                )
    result_effect = defaults.get("results", {}).get("effect", "STALE")
    for source, target in cross_edges:
        edges[source].append((target, result_effect))
    return edges


def trace_impact(
    seeds: dict[Node, set[str]], edges: dict[Node, list[tuple[Node, str]]]
) -> tuple[dict[Node, str], dict[Node, set[str]]]:
    status: dict[Node, str] = {node: "CHANGED" for node in seeds}
    origins: dict[Node, set[str]] = {node: set(paths) for node, paths in seeds.items()}
    queue: deque[Node] = deque(seeds)

    while queue:
        source = queue.popleft()
        for target, effect in edges.get(source, []):
            existing = status.get(target)
            changed = existing is None or STATUS_RANK[effect] > STATUS_RANK[existing]
            combined_origins = origins.get(target, set()) | origins[source]
            if combined_origins != origins.get(target, set()):
                origins[target] = combined_origins
                changed = True
            if existing != "CHANGED" and (existing is None or STATUS_RANK[effect] > STATUS_RANK[existing]):
                status[target] = effect
            if changed:
                queue.append(target)
    return status, origins


def listed_paths(
    container: dict[str, Any], category: str, label: str, warnings: list[str]
) -> list[str]:
    paths: list[str] = []
    for index, value in enumerate(sequence(container.get(category), label), start=1):
        normalized = normalize_map_path(value, f"{label}[{index}]", warnings)
        if normalized:
            paths.append(normalized)
    return paths


def index_path(indexes: dict[str, Any], name: str, warnings: list[str]) -> str | None:
    if name not in indexes:
        return None
    return normalize_map_path(indexes.get(name), f"indexes.{name}", warnings)


def target_details(
    node: Node,
    common: dict[str, Any],
    questions: dict[str, Any],
    indexes: dict[str, Any],
    warnings: list[str],
) -> dict[str, Any]:
    scope, category = node
    question = mapping(questions.get(scope), f"questions.{scope}") if scope in questions else {}
    container = common if scope == "common" else question
    paths: list[str] = []
    claim_ids: list[str] = []
    citation_keys: list[str] = []

    if category in PATH_CATEGORIES:
        paths.extend(listed_paths(container, category, f"{scope}.{category}", warnings))
    if category == "evidence":
        for name in ("claims", "literature"):
            path = index_path(indexes, name, warnings)
            if path:
                paths.append(path)
        evidence = mapping(question.get("evidence"), f"questions.{scope}.evidence")
        claim_ids = [
            str(item)
            for item in sequence(
                evidence.get("claim_ids"), f"questions.{scope}.evidence.claim_ids"
            )
        ]
        citation_keys = [
            str(item)
            for item in sequence(
                evidence.get("citation_keys"),
                f"questions.{scope}.evidence.citation_keys",
            )
        ]
    elif category in {"paper", "review", "delivery"}:
        path = index_path(indexes, category, warnings)
        if path:
            paths.append(path)

    return {
        "scope": scope,
        "category": category,
        "paths": list(dict.fromkeys(paths)),
        "claim_ids": claim_ids,
        "citation_keys": citation_keys,
    }


def ordered_impacts(
    desired_status: str,
    status: dict[Node, str],
    origins: dict[Node, set[str]],
    common: dict[str, Any],
    questions: dict[str, Any],
    indexes: dict[str, Any],
    warnings: list[str],
) -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = []
    for node in sorted(status, key=lambda item: (item[0], ALL_CATEGORIES.index(item[1]))):
        if status[node] != desired_status:
            continue
        details = target_details(node, common, questions, indexes, warnings)
        details["triggered_by"] = sorted(origins.get(node, set()))
        items.append(details)
    return items


def text_report(report: dict[str, Any]) -> str:
    lines = [f"Impact analysis: {report['mode']}", f"Project: {report['project']}", "Changed:"]
    lines.extend(f"- {path}" for path in report["changed"])
    lines.append("\nClassified:")
    if report["matched"]:
        lines.extend(
            f"- {item['path']} -> {item['scope']}.{item['category']} [{item['source']}]"
            for item in report["matched"]
        )
    else:
        lines.append("- none")
    for heading, key in (("STALE (regenerate)", "stale"), ("RECHECK", "recheck")):
        lines.append(f"\n{heading}:")
        if not report[key]:
            lines.append("- none")
            continue
        for item in report[key]:
            lines.append(f"- {item['scope']}.{item['category']}")
            if item["paths"]:
                lines.append("  paths: " + ", ".join(item["paths"]))
            references = item["claim_ids"] + item["citation_keys"]
            if references:
                lines.append("  refs: " + ", ".join(references))
            lines.append("  triggered_by: " + ", ".join(item["triggered_by"]))
    if report["warnings"]:
        lines.append("\nWarnings:")
        lines.extend(f"- {warning}" for warning in report["warnings"])
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Trace transitive downstream impact from changed project-relative files."
    )
    parser.add_argument("project", type=Path, help="formal project root")
    parser.add_argument(
        "--changed", nargs="+", required=True, help="one or more changed or deleted file paths"
    )
    parser.add_argument("--format", choices=("text", "json"), default="text")
    args = parser.parse_args()

    project = args.project.resolve()
    if not project.is_dir():
        parser.error(f"project does not exist: {project}")

    try:
        changed = list(dict.fromkeys(normalize_changed_path(value, project) for value in args.changed))
        artifact_map, warnings, map_exists = load_artifact_map(project)
        defaults = parse_impact_defaults(artifact_map.get("impact_defaults"), warnings)
        registry, common, questions, indexes = build_registry(artifact_map, warnings)
        initial_question_ids = [str(item).lower() for item in questions]
        seeds, matches, question_ids, sources = classify_changes(
            changed, registry, initial_question_ids, warnings
        )
        edges = build_edges(question_ids, defaults, questions)
        status, origins = trace_impact(seeds, edges)
        stale = ordered_impacts(
            "STALE", status, origins, common, questions, indexes, warnings
        )
        recheck = ordered_impacts(
            "RECHECK", status, origins, common, questions, indexes, warnings
        )
    except ImpactMapError as exc:
        parser.error(str(exc))

    if not sources:
        mode = "unresolved"
    elif not map_exists or sources == {"path-prefix"}:
        mode = "inferred"
    elif "path-prefix" in sources:
        mode = "mixed"
    else:
        mode = "mapped"
    report = {
        "project": str(project),
        "map": MAP_RELATIVE_PATH.as_posix() if map_exists else None,
        "mode": mode,
        "changed": changed,
        "matched": matches,
        "stale": stale,
        "recheck": recheck,
        "warnings": list(dict.fromkeys(warnings)),
    }
    if args.format == "json":
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print(text_report(report))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
