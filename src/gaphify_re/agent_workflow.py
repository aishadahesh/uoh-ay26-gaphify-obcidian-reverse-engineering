"""Graph-guided agent workflow with an optional LangGraph adapter."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from .token_meter import estimate_tokens


@dataclass
class InvestigationState:
    question: str
    repo_root: Path
    evidence: list[str] = field(default_factory=list)
    suspected_files: list[Path] = field(default_factory=list)
    root_cause: str = ""
    fix_summary: str = ""
    token_estimate: int = 0


def load_graph_context(state: InvestigationState) -> InvestigationState:
    for relative in ["obsidian/index.md", "obsidian/hot.md", "reports/GRAPH_REPORT.md"]:
        text = (state.repo_root / relative).read_text(encoding="utf-8")
        state.evidence.append(f"# {relative}\n{text}")
        state.token_estimate += estimate_tokens(text)
    return state


def choose_suspects(state: InvestigationState) -> InvestigationState:
    state.suspected_files = [
        state.repo_root / "reports/BROKEN_PYTHON_REPAIR_MATRIX.md",
        state.repo_root / "tests/test_broken_python_fixed.py",
        state.repo_root / "fixed/broken-python/mathsquiz/quiz_core.py",
        state.repo_root / "fixed/broken-python/polygons/polygons.py",
    ]
    return state


def inspect_suspects(state: InvestigationState) -> InvestigationState:
    for path in state.suspected_files:
        text = path.read_text(encoding="utf-8")
        state.evidence.append(f"# {path.name}\n{text}")
        state.token_estimate += estimate_tokens(text)
    state.root_cause = "The selected broken-python files contain syntax failures, global score coupling, and hard-coded polygon logic."
    return state


def explain_fix(state: InvestigationState) -> InvestigationState:
    state.fix_summary = "The fixed copy separates pure logic from interaction, removes global score coupling, and implements general polygon formulas."
    return state


def run_workflow(repo_root: Path, question: str) -> InvestigationState:
    state = InvestigationState(question=question, repo_root=repo_root)
    for step in [load_graph_context, choose_suspects, inspect_suspects, explain_fix]:
        state = step(state)
    return state


def build_langgraph_workflow():
    """Return a LangGraph StateGraph when langgraph is installed."""
    try:
        from langgraph.graph import END, StateGraph
    except ImportError as exc:
        raise RuntimeError("Install the optional 'agent' extra to use LangGraph.") from exc

    graph = StateGraph(InvestigationState)
    graph.add_node("load_graph_context", load_graph_context)
    graph.add_node("choose_suspects", choose_suspects)
    graph.add_node("inspect_suspects", inspect_suspects)
    graph.add_node("explain_fix", explain_fix)
    graph.set_entry_point("load_graph_context")
    graph.add_edge("load_graph_context", "choose_suspects")
    graph.add_edge("choose_suspects", "inspect_suspects")
    graph.add_edge("inspect_suspects", "explain_fix")
    graph.add_edge("explain_fix", END)
    return graph.compile()
