# Experiment Patterns

Use this structure for exploratory and experimental work:

- Title and objective: state the question and the success criteria.
- Setup and reproducibility: import only what you need and keep configuration in one short cell; random-seed and other reproducibility controls follow `docs/standards/data-reproducibility.md`.
- Plan: list hypotheses, sweeps, and metrics before running code.
- Minimal baseline: start with the smallest runnable example and confirm it runs end-to-end before adding complexity.
- Results and notes: summarize findings in markdown near the relevant code and record key metrics in a small dictionary or table-like structure.
- Next steps: decide whether to continue, pivot, or stop, and capture follow-up ideas as short bullets.
