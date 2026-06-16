"""Domain objects for the investigated scheduler project."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class Task:
    """A planned unit of work with a duration and dependency ids."""

    task_id: str
    title: str
    duration_hours: int
    depends_on: tuple[str, ...] = ()

    def finish_time(self, starts_at: int, dependency_finishes: dict[str, int]) -> int:
        """Return the earliest finish time after all dependencies are complete."""
        dependency_ready = max((dependency_finishes[item] for item in self.depends_on), default=starts_at)
        return max(starts_at, dependency_ready) + self.duration_hours


@dataclass
class ProjectPlan:
    """A collection of tasks that can be scheduled in dependency order."""

    tasks: dict[str, Task] = field(default_factory=dict)

    def add(self, task: Task) -> None:
        if task.task_id in self.tasks:
            raise ValueError(f"duplicate task id: {task.task_id}")
        self.tasks[task.task_id] = task

    def roots(self) -> list[Task]:
        return [task for task in self.tasks.values() if not task.depends_on]
