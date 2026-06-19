# EX04 Knowledge Vault Index

## Navigation

- [[hot]] - focused context for the investigated bug.
- [[architecture]] - extracted architecture and diagrams.
- [[bug-investigation]] - symptom, root cause, and fix path.
- [[agent-workflow]] - graph-guided AI agent workflow.
- [[token-efficiency]] - baseline versus graph-guided comparison.
- [[extensions]] - original additions beyond the minimum assignment.

## System Overview

The project reverse-engineers a small Python task scheduler. Raw task lines are parsed into `Task` objects, collected into a `ProjectPlan`, ordered topologically, and converted into finish times. A local AST graph builder creates `artifacts/graph.json`, and the Obsidian vault turns that graph into navigable investigation knowledge.

## Main Research Questions

- What is the real architecture behind a simple-looking parser bug?
- Which module is central to correctness?
- Where could mixed responsibility or hidden complexity appear?
- How does graph-guided navigation reduce unnecessary source reading?
- What changed before and after the fix?

## Rubric Evidence

- [[../reports/ASSIGNMENT_COMPLIANCE.md]] - direct requirement-to-evidence map.
- [[../reports/GRAPH_REPORT.md]] - Grphify-compatible graph evidence.
- [[../reports/TOKEN_EFFICIENCY.md]] - naive, graph-guided, and minimal token proof.
