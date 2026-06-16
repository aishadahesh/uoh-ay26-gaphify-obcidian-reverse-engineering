"""Parsing for the small upstream scheduler chosen for the bug investigation."""

from __future__ import annotations

from .domain import ProjectPlan, Task


class ParseError(ValueError):
    """Raised when the task input cannot be converted into a project plan."""


def parse_task_line(line: str) -> Task:
    """Parse one pipe-delimited task line.

    Format: ``task_id | title | duration_hours | dep_a,dep_b``.
    The dependency column may be empty.
    """
    parts = [part.strip() for part in line.split("|")]
    if len(parts) != 4:
        raise ParseError(f"expected 4 columns, got {len(parts)}: {line!r}")

    task_id, title, duration_text, dependencies_text = parts
    if not task_id or not title:
        raise ParseError(f"task id and title are required: {line!r}")

    try:
        duration = int(duration_text)
    except ValueError as exc:
        raise ParseError(f"duration must be an integer: {duration_text!r}") from exc
    if duration <= 0:
        raise ParseError(f"duration must be positive: {duration}")

    dependencies = tuple(item.strip() for item in dependencies_text.split(",") if item.strip())
    return Task(task_id=task_id, title=title, duration_hours=duration, depends_on=dependencies)


def parse_plan(text: str) -> ProjectPlan:
    """Parse a plan with a two-pass dependency validation strategy.

    The upstream bug validated dependencies while reading each row. That rejected
    valid plans where a task referenced a dependency declared later in the file.
    """
    tasks = [parse_task_line(line) for line in _meaningful_lines(text)]
    known_ids = {task.task_id for task in tasks}
    missing = sorted({dep for task in tasks for dep in task.depends_on if dep not in known_ids})
    if missing:
        raise ParseError(f"unknown dependencies: {', '.join(missing)}")

    plan = ProjectPlan()
    for task in tasks:
        plan.add(task)
    return plan


def _meaningful_lines(text: str) -> list[str]:
    return [line for line in (row.strip() for row in text.splitlines()) if line and not line.startswith("#")]
