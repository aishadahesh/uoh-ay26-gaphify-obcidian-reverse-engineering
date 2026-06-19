# GRAPH_REPORT.md - Grphify-Compatible Graph Analysis

## What Was Generated

The project uses `src/gaphify_re/grphify_runner.py` as a local Grphify-compatible runner. It produces the required graph artifacts without spending LLM tokens on raw source parsing:

- `artifacts/graph.json`
- `artifacts/grphify_summary.json`
- this `reports/GRAPH_REPORT.md`

Current graph output:

| Metric | Value |
|---|---:|
| Nodes | 60 |
| Edges | 192 |
| Extracted edges | 187 |
| Inferred repair edges | 5 |

## Evidence Scale

| Evidence type | Meaning in this project | Count |
|---|---|---:|
| `extracted` | AST-detected calls and containment relationships. This is deterministic and token-free. | 187 |
| `inferred` | Human/agent repair mapping from upstream broken file to fixed file. | 5 |
| `ambiguous` | Reserved for uncertain links that require human review. None are currently kept in the final graph. | 0 |

## Central Nodes

| Node | Why it matters |
|---|---|
| `gaphify_re/cli.py::main` | Connects graph, CrewAI-style agent, token proof, and demo commands. |
| `gaphify_re/graph_builder.py::build_graph` | Core deterministic AST graph extraction. |
| `mathsquiz/quiz_core.py::run_quiz` | Main fixed quiz workflow and scoring route. |
| `polygons/polygons.py::draw_polygon` | Uses fixed polygon side count and exterior angle logic. |
| `gaphify_re/parser.py::parse_plan` | Auxiliary parser bug example retained for comparison and tests. |

## Communities

| Community | Files | Responsibility |
|---|---|---|
| Upstream evidence | `data/upstream_broken_python/` | Broken source files selected from `martinpeck/broken-python`. |
| Fixed implementation | `fixed/broken-python/` | Repaired quiz and polygon scripts. |
| Grphify layer | `graph_builder.py`, `grphify_runner.py`, `artifacts/graph.json` | Structural graph extraction and summary. |
| Agent and token layer | `crew_agent.py`, `agent_workflow.py`, `token_meter.py` | Graph-first investigation and context budgeting. |
| Documentation layer | `obsidian/`, `reports/`, `docs/`, `README.md` | Human-readable knowledge vault and submission proof. |

## God Nodes And Risk

No severe God Node remains in the fixed upstream code. The highest-centrality fixed-code node is `run_quiz`, but it delegates question representation, answer checking, and final scoring to smaller functions. The original upstream risk was the opposite: many repeated inline quiz blocks with no reusable boundary.

## Graph-Guided Debugging Value

The graph first points the agent to the hot repair route:

`artifacts/grphify_summary.json` -> `obsidian/index.md` -> `obsidian/hot.md` -> `reports/BROKEN_PYTHON_REPAIR_MATRIX.md`

Only after this route does the agent read selected code and tests. This implements the assignment's requirement that the agent rely first on Grphify/Obsidian outputs and only then request relevant code snippets.
