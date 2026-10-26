"""Core storage and task logic for todo-cli."""

from __future__ import annotations

import json
import os
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path


def default_path() -> Path:
    """Where tasks are stored. Override with the TODO_FILE environment variable."""
    env = os.environ.get("TODO_FILE")
    return Path(env) if env else Path.home() / ".todo.json"


@dataclass
class Task:
    id: int
    text: str
    done: bool = False
    created: str = ""

    def __post_init__(self) -> None:
        if not self.created:
            self.created = datetime.now(timezone.utc).isoformat(timespec="seconds")


class TodoList:
    def __init__(self, path: Path | None = None) -> None:
        self.path = Path(path) if path else default_path()
        self.tasks: list[Task] = []
        self._load()

    def _load(self) -> None:
        if not self.path.exists():
            return
        try:
            data = json.loads(self.path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            raise ValueError(f"{self.path} is not valid JSON: {exc}") from exc
        self.tasks = [Task(**item) for item in data]

    def save(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        payload = json.dumps([asdict(t) for t in self.tasks], indent=2)
        self.path.write_text(payload + "\n", encoding="utf-8")

    def _next_id(self) -> int:
        return max((t.id for t in self.tasks), default=0) + 1

    def _find(self, task_id: int) -> Task:
        for task in self.tasks:
            if task.id == task_id:
                return task
        raise KeyError(f"No task with id {task_id}")

    def add(self, text: str) -> Task:
        text = text.strip()
        if not text:
            raise ValueError("Task text cannot be empty")
        task = Task(id=self._next_id(), text=text)
        self.tasks.append(task)
        self.save()
        return task

    def complete(self, task_id: int) -> Task:
        task = self._find(task_id)
        task.done = True
        self.save()
        return task

    def remove(self, task_id: int) -> Task:
        task = self._find(task_id)
        self.tasks.remove(task)
        self.save()
        return task

    def clear_done(self) -> int:
        before = len(self.tasks)
        self.tasks = [t for t in self.tasks if not t.done]
        self.save()
        return before - len(self.tasks)

    def list(self, show_done: bool = True) -> list[Task]:
        return [t for t in self.tasks if show_done or not t.done]
