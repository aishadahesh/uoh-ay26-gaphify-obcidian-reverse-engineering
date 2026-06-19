"""Local Grphify-compatible graph outputs for the EX04 project."""

from __future__ import annotations

import json
from pathlib import Path

from .graph_builder import build_graph

FIXED_MAP = {
    "mathsquiz/mathsquiz.py": "fixed/broken-python/mathsquiz/mathsquiz.py",
    "mathsquiz/mathsquiz-step1.py": "fixed/broken-python/mathsquiz/mathsquiz-step1.py",
    "mathsquiz/mathsquiz-step2.py": "fixed/broken-python/mathsquiz/mathsquiz-step2.py",
    "mathsquiz/mathsquiz-step3.py": "fixed/broken-python/mathsquiz/mathsquiz-step3.py",
    "polygons/polygons.py": "fixed/broken-python/polygons/polygons.py",
}


def build_grphify_graph(repo_root: Path) -> dict:
    """Build a Grphify-style graph over tooling and fixed upstream code."""
    roots = [repo_root / "src", repo_root / "fixed" / "broken-python"]
    graphs = [build_graph(root) for root in roots]
    nodes = [node for graph in graphs for node in graph["nodes"]]
    edges = [_with_evidence(edge, "extracted", 1.0) for graph in graphs for edge in graph["edges"]]
    edges.extend(_repair_edges(repo_root))
    return {
        "metadata": {
            "tool": "local-grphify-compatible",
            "purpose": "EX04 graph-guided reverse engineering",
            "evidence_scale": ["extracted", "inferred", "ambiguous"],
        },
        "nodes": sorted(nodes, key=lambda item: item["id"]),
        "edges": sorted(edges, key=lambda item: (item["source"], item["target"], item["type"])),
    }


def write_grphify_outputs(repo_root: Path) -> dict:
    """Write graph.json and a compact summary for agents and reports."""
    graph = build_grphify_graph(repo_root)
    artifacts = repo_root / "artifacts"
    artifacts.mkdir(parents=True, exist_ok=True)
    (artifacts / "graph.json").write_text(json.dumps(graph, indent=2), encoding="utf-8")
    summary = summarize_graph(graph)
    (artifacts / "grphify_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    return graph


def summarize_graph(graph: dict) -> dict:
    """Return centrality and evidence totals for token-light navigation."""
    central = sorted(graph["nodes"], key=lambda item: item.get("centrality", 0), reverse=True)[:8]
    evidence_counts: dict[str, int] = {}
    for edge in graph["edges"]:
        evidence_counts[edge["evidence"]] = evidence_counts.get(edge["evidence"], 0) + 1
    return {
        "node_count": len(graph["nodes"]),
        "edge_count": len(graph["edges"]),
        "evidence_counts": evidence_counts,
        "central_nodes": central,
        "minimal_route": ["obsidian/index.md", "obsidian/hot.md", "reports/BROKEN_PYTHON_REPAIR_MATRIX.md"],
    }


def _with_evidence(edge: dict, evidence: str, confidence: float) -> dict:
    return edge | {"evidence": evidence, "confidence": confidence}


def _repair_edges(repo_root: Path) -> list[dict]:
    edges: list[dict] = []
    for upstream, fixed in FIXED_MAP.items():
        edges.append(
            {
                "source": f"data/upstream_broken_python/{upstream}",
                "target": fixed,
                "type": "repairs",
                "evidence": "inferred",
                "confidence": 0.85,
            }
        )
    if not (repo_root / "tests" / "test_broken_python_fixed.py").exists():
        edges.append(
            {
                "source": "tests/test_broken_python_fixed.py",
                "target": "fixed/broken-python",
                "type": "verifies",
                "evidence": "ambiguous",
                "confidence": 0.4,
            }
        )
    return edges
