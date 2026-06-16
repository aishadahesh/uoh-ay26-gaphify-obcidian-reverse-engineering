"""AST-based graph extraction similar in spirit to Grphify."""

from __future__ import annotations

import ast
import json
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class CodeNode:
    id: str
    kind: str
    file: str
    name: str


class _Visitor(ast.NodeVisitor):
    def __init__(self, file_path: Path, package_root: Path) -> None:
        self.file_path = file_path
        self.package_root = package_root
        self.nodes: dict[str, CodeNode] = {}
        self.edges: set[tuple[str, str, str]] = set()
        self.scope: list[str] = []

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        node_id = self._id(node.name)
        self.nodes[node_id] = CodeNode(node_id, "class", self._rel(), node.name)
        self._with_scope(node_id, node)

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        node_id = self._id(node.name)
        kind = "method" if self.scope and self.nodes[self.scope[-1]].kind == "class" else "function"
        self.nodes[node_id] = CodeNode(node_id, kind, self._rel(), node.name)
        if self.scope:
            self.edges.add((self.scope[-1], node_id, "contains"))
        self._with_scope(node_id, node)

    def visit_Call(self, node: ast.Call) -> None:
        if self.scope:
            called = _call_name(node.func)
            if called:
                self.edges.add((self.scope[-1], called, "calls"))
        self.generic_visit(node)

    def _with_scope(self, node_id: str, node: ast.AST) -> None:
        self.scope.append(node_id)
        self.generic_visit(node)
        self.scope.pop()

    def _id(self, name: str) -> str:
        return f"{self._rel()}::{'.'.join([*self.scope, name]) if self.scope else name}"

    def _rel(self) -> str:
        return self.file_path.relative_to(self.package_root).as_posix()


def build_graph(source_root: Path) -> dict:
    """Build a deterministic graph.json from Python source files."""
    all_nodes: dict[str, CodeNode] = {}
    all_edges: set[tuple[str, str, str]] = set()
    for path in sorted(source_root.rglob("*.py")):
        tree = ast.parse(path.read_text(encoding="utf-8"))
        visitor = _Visitor(path, source_root)
        visitor.visit(tree)
        all_nodes.update(visitor.nodes)
        all_edges.update(visitor.edges)

    nodes = [node.__dict__ | {"centrality": 0} for node in all_nodes.values()]
    centrality: dict[str, int] = {node["id"]: 0 for node in nodes}
    for source, target, _kind in all_edges:
        centrality[source] = centrality.get(source, 0) + 1
        centrality[target] = centrality.get(target, 0) + 1
    for node in nodes:
        node["centrality"] = centrality.get(node["id"], 0)

    return {
        "metadata": {"tool": "local-ast-grphify", "source_root": str(source_root)},
        "nodes": sorted(nodes, key=lambda item: item["id"]),
        "edges": [{"source": s, "target": t, "type": k} for s, t, k in sorted(all_edges)],
    }


def write_graph(source_root: Path, output_path: Path) -> dict:
    graph = build_graph(source_root)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(graph, indent=2), encoding="utf-8")
    return graph


def _call_name(node: ast.AST) -> str | None:
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        return node.attr
    return None
