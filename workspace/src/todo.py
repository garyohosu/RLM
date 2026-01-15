from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Optional
import json


@dataclass
class TodoItem:
    id: int
    title: str
    completed: bool = False


class TodoList:
    def __init__(self) -> None:
        self._items: dict[int, TodoItem] = {}
        self._next_id: int = 1

    def add_task(self, title: str) -> TodoItem:
        """Add a new task and return it."""
        item = TodoItem(id=self._next_id, title=title)
        self._items[self._next_id] = item
        self._next_id += 1
        return item

    def list_tasks(self) -> list[TodoItem]:
        """Return all tasks."""
        return list(self._items.values())

    def complete_task(self, task_id: int) -> Optional[TodoItem]:
        """Mark a task as completed. Returns None if not found."""
        item = self._items.get(task_id)
        if item is not None:
            item.completed = True
        return item

    def delete_task(self, task_id: int) -> bool:
        """Delete a task. Returns True if deleted, False if not found."""
        if task_id in self._items:
            del self._items[task_id]
            return True
        return False

    def save(self, path: Path) -> None:
        """Save todos to a JSON file."""
        data = {
            "items": [asdict(item) for item in self._items.values()],
            "next_id": self._next_id,
        }
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2))

    @classmethod
    def load(cls, path: Path) -> "TodoList":
        """Load todos from a JSON file."""
        data = json.loads(path.read_text())
        todo_list = cls()
        for item_data in data["items"]:
            item = TodoItem(**item_data)
            todo_list._items[item.id] = item
        todo_list._next_id = data["next_id"]
        return todo_list
