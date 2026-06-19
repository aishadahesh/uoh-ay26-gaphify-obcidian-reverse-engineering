# Token Efficiency Report

## What Is Being Measured

The assignment asks for an AI agent that finds bugs while avoiding unnecessary context. Therefore this report treats token efficiency as **the size of the prompt context sent to the AI bug-finding agent**, not just the number of files in the repository.

The project supports two related flows:

```powershell
python -m gaphify_re gemini-prompt --repo . --mode minimal
python -m gaphify_re gemini --repo . --mode minimal
```

`gemini-prompt` is safe and local: it builds the exact prompt packet and estimates prompt tokens without calling the API. `gemini` sends that packet to Gemini, requires `GEMINI_API_KEY`, and persists the latest result to:

```text
artifacts/gemini_agent_result.json
reports/GEMINI_AGENT_REPORT.md
```

## Gemini Agent Prompt Comparison

| Agent mode | Files sent to Gemini | Estimated prompt tokens | Iterations | Purpose |
|---|---:|---:|---:|---|
| Naive agent prompt | 8 | 5,379 | 5 | Sends broad upstream/fixed/test context before narrowing suspects. |
| Graph-guided agent prompt | 5 | 3,042 | 2 | Sends Grphify summary, `index.md`, `hot.md`, repair matrix, and tests. |
| Minimal agent prompt | 3 | 1,424 | 1 | Smallest Gemini packet that still names suspects, root causes, fixes, and evidence. |

## Reproduction Commands

```powershell
python -m gaphify_re gemini-prompt --repo . --mode naive
python -m gaphify_re gemini-prompt --repo . --mode graph-guided
python -m gaphify_re gemini-prompt --repo . --mode minimal
```

The measured outputs are:

```text
naive:         5,379 estimated prompt tokens, 8 files
graph-guided: 3,042 estimated prompt tokens, 5 files
minimal:      1,424 estimated prompt tokens, 3 files
```

## Minimal Prompt Packet

The minimal Gemini prompt includes only:

1. `artifacts/grphify_summary.json` - central graph facts, evidence counts, and navigation route.
2. `obsidian/hot.md` - focused context for the selected broken-python bug family.
3. `reports/BROKEN_PYTHON_REPAIR_MATRIX.md` - exact upstream file, root cause, fixed file, and verification test mapping.

This is enough for the AI agent to identify the hot files and explain the repairs without reading every raw source file.

## Why The Minimal Packet Works

The minimal packet works because the expensive thinking has already been structured:

- Grphify-compatible graph output identifies central files and repair edges.
- `hot.md` narrows the investigation to the bug-critical area.
- The repair matrix states the before/after evidence and points to tests.

The agent is not asked to discover the whole repository from scratch. It receives a compact navigation layer first, then can request more source only if needed.

## Savings

Compared with the naive Gemini prompt:

| Comparison | Token saving |
|---|---:|
| Graph-guided vs naive | about 43% |
| Minimal vs naive | about 74% |

This satisfies the assignment requirement to compare naive work against graph-guided work using token count, files/context units read, iterations, and quality of root-cause discovery.

## Agent Iteration Comparison

| Mode | Iteration 1 | Later iterations | Root-cause quality |
|---|---|---|---|
| Naive | Reads many raw files first. | Must infer which files matter after seeing broad context. | Correct but wasteful. |
| Graph-guided | Reads graph summary, `index.md`, and `hot.md`. | Reads repair matrix and tests. | Correct and focused. |
| Minimal | Reads only graph summary, `hot.md`, and repair matrix. | No extra iteration needed for the documented bug family. | Correct for known selected bugs. |

## Supporting Local Reading Estimate

The local file-reading estimator still exists for reproducibility and for non-API runs:

| Local mode | Files read | Estimated tokens | Iterations |
|---|---:|---:|---:|
| Naive raw-code reading | 17 | 7,913 | 5 |
| Graph-guided reading | 5 | 2,908 | 2 |
| Minimal-sufficient packet | 3 | 1,312 | 1 |

The Gemini prompt numbers are the primary assignment evidence because they represent the context an AI bug-finding agent actually consumes. The local numbers are supporting evidence for the same navigation pattern.

## API Key Safety

Do not put a real Gemini key in Git or hard-code it in `.venv`. Use one of these local-only options:

```powershell
$env:GEMINI_API_KEY="your_key_here"
$env:GEMINI_MODEL="gemini-2.5-flash"
```

or copy `.env.example` to `.env` for your own machine. `.env` is ignored by Git.

## Persisted AI-Agent Evidence

After a successful API run:

```powershell
python -m gaphify_re gemini --repo . --mode minimal
```

these files are updated:

```text
artifacts/gemini_agent_result.json
reports/GEMINI_AGENT_REPORT.md
```

Those files provide the concrete evidence that the AI agent used the minimal graph-guided packet and returned a bug/root-cause analysis.
