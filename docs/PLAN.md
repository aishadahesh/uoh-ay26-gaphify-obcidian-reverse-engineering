# PLAN - Architecture And Workflow

## Architecture

```mermaid
flowchart LR
    Upstream[data/upstream_broken_python] --> Grphify[local Grphify-compatible graph]
    Grphify --> Artifacts[graph.json and grphify_summary.json]
    Artifacts --> Obsidian[index.md and hot.md]
    Obsidian --> Crew[CrewAI-style agent]
    Crew --> Gemini[Gemini API agent]
    Gemini --> AgentReports[gemini_agent_result.json and GEMINI_AGENT_REPORT.md]
    Crew --> Fixed[fixed/broken-python]
    Fixed --> Tests[before/after tests]
    Tests --> Reports[reports and README]
```

## Key Decisions

- Use a deterministic local graph runner so graph creation costs no LLM tokens.
- Preserve optional real CrewAI/LangGraph adapters without requiring network installs for normal grading.
- Keep `hot.md` and `grphify_summary.json` as the minimal context packet.
- Use file-by-file tests to prove both original failures and repaired behavior.

## Trade-Offs

The project does not require the external Grphify binary at runtime. Instead, it produces Grphify-compatible outputs using AST extraction and explicit evidence labels. This keeps the submission reproducible in a clean Python environment while matching the assignment's graph-first workflow.

## Gemini Evidence Persistence

The `gemini` CLI command writes the latest API execution to `artifacts/gemini_agent_result.json` and `reports/GEMINI_AGENT_REPORT.md`. This makes the AI-agent result auditable instead of only visible in terminal output.
