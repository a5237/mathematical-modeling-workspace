---
name: "jupyter-notebook"
description: "Use when the user asks to create, scaffold, or edit Jupyter notebooks (`.ipynb`) for experiments, explorations, or tutorials; prefer the bundled templates and run the helper script `new_notebook.py` to generate a clean starting notebook."
---


# Jupyter Notebook Skill

Create clean, reproducible Jupyter notebooks for two primary modes:

- Experiments and exploratory analysis
- Tutorials and teaching-oriented walkthroughs

Prefer the bundled templates and the helper script for consistent structure and fewer JSON mistakes.

## When to use
- Create a new `.ipynb` notebook from scratch.
- Convert rough notes or scripts into a structured notebook.
- Refactor an existing notebook to be more reproducible and skimmable.
- Build experiments or tutorials that will be read or re-run by other people.

## Decision tree
- If the request is exploratory, analytical, or hypothesis-driven, choose `experiment`.
- If the request is instructional, step-by-step, or audience-specific, choose `tutorial`.
- If editing an existing notebook, treat it as a refactor: preserve intent and improve structure.

## Skill path (set once)

```bash
export CODEX_HOME="${CODEX_HOME:-$HOME/.codex}"
export JUPYTER_NOTEBOOK_CLI="$CODEX_HOME/skills/jupyter-notebook/scripts/new_notebook.py"
```

User-scoped skills install under `$CODEX_HOME/skills` (default: `~/.codex/skills`).

## Workflow
1. Lock the intent.
Identify the notebook kind: `experiment` or `tutorial`.
Capture the objective, audience, and what "done" looks like.

2. Scaffold from the template.
Use the helper script to avoid hand-authoring raw notebook JSON: invoke `$JUPYTER_NOTEBOOK_CLI` with `--kind` (`experiment` or `tutorial`), `--title`, and `--out`.
Run it with the workspace's locked Python environment; the interpreter, installation and dependency authority is `docs/guides/modeling-environment.md` with `config/python/requirements-modeling.txt`. This skill defines no separate install or run commands.

3. Fill the notebook with small, runnable steps.
Keep each code cell focused on one step.
Add short markdown cells that explain the purpose and expected result.
Avoid large, noisy outputs when a short summary works.

4. Apply the right pattern.
For experiments, follow `references/experiment-patterns.md`.
For tutorials, follow `references/tutorial-patterns.md`.

5. Edit safely when working with existing notebooks.
Preserve the notebook structure; avoid reordering cells unless it improves the top-to-bottom story.
Prefer targeted edits over full rewrites.
If you must edit raw JSON, review `references/notebook-structure.md` first.

6. Validate the result.
Use the final pass checklist in `references/quality-checklist.md`; it is the only place that lists the validation steps.

## Templates and helper script
- Templates live in `assets/experiment-template.ipynb` and `assets/tutorial-template.ipynb`.
- The helper script loads a template, updates the title cell, and writes a notebook.

Script path:
- `$JUPYTER_NOTEBOOK_CLI` (installed default: `$CODEX_HOME/skills/jupyter-notebook/scripts/new_notebook.py`)

## Temp and output conventions
- Use `var/temp/jupyter-notebook/` for intermediate files; delete when done.
- Place notebooks only at locations allowed by `LAYOUT-001` (`docs/architecture/workspace-layout.md`): notebooks feeding the formal chain go in the corresponding `03-models/<question>/` directory, exploratory notebooks go in `sandbox/` under `WG-TEST-001`. This skill defines no project directory of its own.
- Name notebooks per `docs/standards/naming.md`.

## Dependencies (install only when needed)
All Python dependencies are installed and locked through the workspace environment authority in `docs/guides/modeling-environment.md` and `config/python/requirements-modeling.txt`; this skill adds no installation method of its own.
The bundled scaffold script uses only the Python standard library and does not require extra dependencies.

## Environment
No required environment variables.

## Reference map
- `references/experiment-patterns.md`: experiment structure and heuristics.
- `references/tutorial-patterns.md`: tutorial structure and teaching flow.
- `references/notebook-structure.md`: notebook JSON shape and safe editing rules.
- `references/quality-checklist.md`: final validation checklist.
