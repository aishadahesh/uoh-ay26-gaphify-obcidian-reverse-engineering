"""CrewAI-oriented bug-hunting workflow with a deterministic local runner."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .token_meter import estimate_tokens


@dataclass(frozen=True)
class CrewStep:
    role: str
    goal: str
    artifact: str


@dataclass(frozen=True)
class CrewResult:
    root_cause: str
    fix_summary: str
    files_read: tuple[str, ...]
    estimated_tokens: int
    steps: tuple[CrewStep, ...]


CREW_STEPS = (
    CrewStep("Graph Navigator", "Start with Grphify outputs, index.md, and hot.md", "artifacts/grphify_summary.json"),
    CrewStep("Bug Investigator", "Read only the hot upstream/fixed evidence", "reports/BROKEN_PYTHON_REPAIR_MATRIX.md"),
    CrewStep("Fix Verifier", "Check before/after tests instead of all raw files", "tests/test_broken_python_fixed.py"),
)


def run_crewai_bug_hunt(repo_root: Path) -> CrewResult:
    """Run the CrewAI-style graph-guided investigation without network calls."""
    paths = [
        "artifacts/grphify_summary.json",
        "obsidian/index.md",
        "obsidian/hot.md",
        "reports/BROKEN_PYTHON_REPAIR_MATRIX.md",
        "tests/test_broken_python_fixed.py",
    ]
    token_total = 0
    for relative in paths:
        token_total += estimate_tokens((repo_root / relative).read_text(encoding="utf-8"))
    return CrewResult(
        root_cause="Syntax failures, global score coupling, and hard-coded polygon logic in the selected broken-python files.",
        fix_summary="Fixed copy adds testable quiz core, parameter-based scoring, valid polygon formulas, and import-safe scripts.",
        files_read=tuple(paths),
        estimated_tokens=token_total,
        steps=CREW_STEPS,
    )


def build_crewai_crew():
    """Build real CrewAI agents when the optional dependency is installed."""
    try:
        from crewai import Agent, Crew, Task
    except ImportError as exc:
        raise RuntimeError("Install the optional 'agent' extra to run real CrewAI objects.") from exc

    navigator = Agent(role="Graph Navigator", goal="Use Grphify and Obsidian context first", backstory="Graph-first debugger")
    investigator = Agent(role="Bug Investigator", goal="Identify root causes from minimal hot files", backstory="Python repair specialist")
    verifier = Agent(role="Fix Verifier", goal="Confirm before/after evidence", backstory="Testing-focused reviewer")
    tasks = [
        Task(description="Read graph and hot context", expected_output="suspect list", agent=navigator),
        Task(description="Explain the broken-python bugs", expected_output="root cause", agent=investigator),
        Task(description="Validate tests and fixes", expected_output="verification summary", agent=verifier),
    ]
    return Crew(agents=[navigator, investigator, verifier], tasks=tasks)
