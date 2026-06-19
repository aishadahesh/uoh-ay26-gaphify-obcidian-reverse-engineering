"""Prompt packets for the Gemini-backed EX04 debugging agent."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .token_meter import estimate_tokens


@dataclass(frozen=True)
class AgentPrompt:
    mode: str
    files: tuple[str, ...]
    prompt: str
    estimated_tokens: int


PROMPT_HEADER = """You are an AI debugging agent for EX04.
Goal: identify bugs, explain root causes, and propose fixes.
Rules:
1. Use Grphify/Obsidian evidence first when available.
2. Request or inspect raw code only after the graph-guided context identifies hot files.
3. Report root cause, fix summary, and verification evidence.
"""


MODE_FILES = {
    "naive": (
        "data/upstream_broken_python/mathsquiz/mathsquiz.py",
        "data/upstream_broken_python/mathsquiz/mathsquiz-step1.py",
        "data/upstream_broken_python/mathsquiz/mathsquiz-step2.py",
        "data/upstream_broken_python/mathsquiz/mathsquiz-step3.py",
        "data/upstream_broken_python/polygons/polygons.py",
        "fixed/broken-python/mathsquiz/quiz_core.py",
        "fixed/broken-python/polygons/polygons.py",
        "tests/test_broken_python_fixed.py",
    ),
    "graph-guided": (
        "artifacts/grphify_summary.json",
        "obsidian/index.md",
        "obsidian/hot.md",
        "reports/BROKEN_PYTHON_REPAIR_MATRIX.md",
        "tests/test_broken_python_fixed.py",
    ),
    "minimal": (
        "artifacts/grphify_summary.json",
        "obsidian/hot.md",
        "reports/BROKEN_PYTHON_REPAIR_MATRIX.md",
    ),
}


def build_agent_prompt(repo_root: Path, mode: str = "minimal") -> AgentPrompt:
    """Build the exact context packet sent to Gemini for one mode."""
    if mode not in MODE_FILES:
        raise ValueError(f"unknown mode: {mode}")
    sections = [PROMPT_HEADER.strip()]
    for relative in MODE_FILES[mode]:
        path = repo_root / relative
        sections.append(f"\n--- FILE: {relative} ---\n{path.read_text(encoding='utf-8')}")
    prompt = "\n".join(sections)
    return AgentPrompt(mode, MODE_FILES[mode], prompt, estimate_tokens(prompt))
