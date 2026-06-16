"""Command-line entry points for the EX04 project."""

from __future__ import annotations

import argparse
from pathlib import Path

from .agent_workflow import run_workflow
from .graph_builder import write_graph
from .parser import parse_plan
from .scheduler import schedule
from .token_meter import compare_modes


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="EX04 graph-guided reverse engineering tools")
    parser.add_argument("command", choices=["graph", "agent", "tokens", "demo"])
    parser.add_argument("--repo", type=Path, default=Path.cwd())
    args = parser.parse_args(argv)

    if args.command == "graph":
        graph = write_graph(args.repo / "src", args.repo / "artifacts" / "graph.json")
        print(f"wrote {len(graph['nodes'])} nodes and {len(graph['edges'])} edges")
        return 0
    if args.command == "agent":
        state = run_workflow(args.repo, "Why did dependency parsing fail?")
        print(state.root_cause)
        print(state.fix_summary)
        print(f"estimated tokens: {state.token_estimate}")
        return 0
    if args.command == "demo":
        text = "deploy | Deploy app | 1 | test\ntest | Run tests | 2 |"
        plan = parse_plan(text)
        print(schedule(plan))
        return 0

    for mode in compare_modes(args.repo):
        print(f"{mode.name}: {mode.estimated_tokens} tokens, {mode.files_read} files, {mode.iterations} iterations")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
