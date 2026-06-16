"""Scheduling algorithms for parsed project plans."""

from __future__ import annotations

from .domain import ProjectPlan, Task


class CycleError(ValueError):
    """Raised when dependencies cannot be resolved into a directed acyclic order."""


def topological_order(plan: ProjectPlan) -> list[Task]:
    """Return tasks in dependency-safe order."""
    remaining = dict(plan.tasks)
    completed: set[str] = set()
    ordered: list[Task] = []

    while remaining:
        ready = sorted(
            [task for task in remaining.values() if set(task.depends_on).issubset(completed)],
            key=lambda task: task.task_id,
        )
        if not ready:
            cycle_nodes = ", ".join(sorted(remaining))
            raise CycleError(f"cycle or unresolved dependency among: {cycle_nodes}")
        for task in ready:
            ordered.append(task)
            completed.add(task.task_id)
            del remaining[task.task_id]
    return ordered


def schedule(plan: ProjectPlan, starts_at: int = 0) -> dict[str, int]:
    """Return task finish times keyed by task id."""
    finishes: dict[str, int] = {}
    for task in topological_order(plan):
        finishes[task.task_id] = task.finish_time(starts_at, finishes)
    return finishes
