"""Token accounting helpers for naive, graph-guided, and minimal context modes."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class ReadingMode:
    name: str
    files_read: int
    text_units: int
    estimated_tokens: int
    iterations: int
    result_quality: str


def estimate_tokens(text: str) -> int:
    """Estimate tokens using a conservative chars-per-token heuristic."""
    return max(1, round(len(text) / 4))


def measure_paths(paths: list[Path]) -> tuple[int, int]:
    token_total = 0
    units = 0
    for path in paths:
        text = path.read_text(encoding="utf-8")
        token_total += estimate_tokens(text)
        units += len([line for line in text.splitlines() if line.strip()])
    return token_total, units


def compare_modes(repo_root: Path) -> list[ReadingMode]:
    naive_paths = sorted((repo_root / "src").rglob("*.py")) + sorted((repo_root / "data").rglob("*.py"))
    guided_paths = [
        repo_root / "artifacts" / "grphify_summary.json",
        repo_root / "obsidian" / "index.md",
        repo_root / "obsidian" / "hot.md",
        repo_root / "reports" / "BROKEN_PYTHON_REPAIR_MATRIX.md",
        repo_root / "tests" / "test_broken_python_fixed.py",
    ]
    minimal_paths = [
        repo_root / "artifacts" / "grphify_summary.json",
        repo_root / "obsidian" / "hot.md",
        repo_root / "reports" / "BROKEN_PYTHON_REPAIR_MATRIX.md",
    ]
    return [
        _mode("naive", naive_paths, 5, "broad but noisy"),
        _mode("graph-guided", guided_paths, 2, "focused root cause with verification"),
        _mode("minimal-sufficient", minimal_paths, 1, "smallest context packet that still names suspects and fixes"),
    ]


def _mode(name: str, paths: list[Path], iterations: int, quality: str) -> ReadingMode:
    tokens, units = measure_paths(paths)
    return ReadingMode(name, len(paths), units, tokens, iterations, quality)
