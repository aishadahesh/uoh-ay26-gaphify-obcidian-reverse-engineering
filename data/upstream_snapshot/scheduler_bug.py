"""Original reduced buggy code selected for reverse engineering."""


def parse_plan(text):
    tasks = {}
    for line in text.splitlines():
        if not line.strip() or line.strip().startswith("#"):
            continue
        task_id, title, duration, deps = [part.strip() for part in line.split("|")]
        dependencies = [item.strip() for item in deps.split(",") if item.strip()]
        for dependency in dependencies:
            if dependency not in tasks:
                raise ValueError(f"unknown dependency: {dependency}")
        tasks[task_id] = {"title": title, "duration": int(duration), "deps": dependencies}
    return tasks
