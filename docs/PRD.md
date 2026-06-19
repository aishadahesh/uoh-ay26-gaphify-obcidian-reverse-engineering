# PRD - EX04 Graph-Guided Broken Python Repair

## Goal

Demonstrate that a graph-guided workflow can reverse-engineer unfamiliar buggy Python code, identify root causes, repair code, verify fixes, and reduce token usage compared with naive raw-code reading.

## Selected Repository

`martinpeck/broken-python` was selected because it contains compact, intentionally broken Python scripts suitable for complete before/after repair evidence.

## Functional Requirements

- Recreate selected upstream broken files locally.
- Provide a fixed copy under `fixed/broken-python/`.
- Generate Grphify-compatible graph artifacts.
- Provide an Obsidian vault with `index.md` and `hot.md`.
- Run a CrewAI-oriented graph-first agent workflow.
- Prove before/after behavior with tests.
- Prove token savings with naive, graph-guided, and minimal Gemini prompt modes.
- Persist Gemini API runs to JSON and Markdown evidence files.

## Acceptance Criteria

- `python -m unittest discover -s tests` passes.
- `python -m gaphify_re graph --repo .` writes `artifacts/graph.json` and `artifacts/grphify_summary.json`.
- `python -m gaphify_re crew --repo .` reports root cause, fix summary, and token estimate.
- `python -m gaphify_re tokens --repo .` prints three token modes.
- `python -m gaphify_re gemini --repo . --mode minimal` writes `artifacts/gemini_agent_result.json` and `reports/GEMINI_AGENT_REPORT.md`.
- README and reports map every assignment requirement to evidence.
