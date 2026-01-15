import pytest
from workspace.src.todo import TodoItem, TodoList


class TestTodoItem:
    def test_create_item(self):
        item = TodoItem(id=1, title="Buy milk")
        assert item.id == 1
        assert item.title == "Buy milk"
        assert item.completed is False


class TestTodoList:
    def test_add_task(self):
        todo_list = TodoList()
        item = todo_list.add_task("Buy milk")
        assert item.id == 1
        assert item.title == "Buy milk"
        assert item.completed is False

    def test_add_multiple_tasks(self):
        todo_list = TodoList()
        item1 = todo_list.add_task("Task 1")
        item2 = todo_list.add_task("Task 2")
        assert item1.id == 1
        assert item2.id == 2

    def test_list_tasks_empty(self):
        todo_list = TodoList()
        assert todo_list.list_tasks() == []

    def test_list_tasks(self):
        todo_list = TodoList()
        todo_list.add_task("Task 1")
        todo_list.add_task("Task 2")
        tasks = todo_list.list_tasks()
        assert len(tasks) == 2

    def test_complete_task(self):
        todo_list = TodoList()
        item = todo_list.add_task("Buy milk")
        completed = todo_list.complete_task(item.id)
        assert completed is not None
        assert completed.completed is True  # This will FAIL

    def test_complete_task_not_found(self):
        todo_list = TodoList()
        result = todo_list.complete_task(999)
        assert result is None

    def test_delete_task(self):
        todo_list = TodoList()
        item = todo_list.add_task("Buy milk")
        deleted = todo_list.delete_task(item.id)
        assert deleted is True
        assert len(todo_list.list_tasks()) == 0  # This will FAIL

    def test_delete_task_not_found(self):
        todo_list = TodoList()
        result = todo_list.delete_task(999)
        assert result is False


class TestTodoPersistence:
    def test_save_creates_file(self, tmp_path):
        todo_list = TodoList()
        todo_list.add_task("Task 1")
        file_path = tmp_path / "todos.json"
        todo_list.save(file_path)
        assert file_path.exists()

    def test_save_content(self, tmp_path):
        import json
        todo_list = TodoList()
        todo_list.add_task("Task 1")
        todo_list.add_task("Task 2")
        todo_list.complete_task(1)
        file_path = tmp_path / "todos.json"
        todo_list.save(file_path)

        data = json.loads(file_path.read_text())
        assert len(data["items"]) == 2
        assert data["items"][0]["id"] == 1
        assert data["items"][0]["title"] == "Task 1"
        assert data["items"][0]["completed"] is True
        assert data["items"][1]["id"] == 2
        assert data["items"][1]["completed"] is False

    def test_load_restores_tasks(self, tmp_path):
        todo_list = TodoList()
        todo_list.add_task("Task 1")
        todo_list.add_task("Task 2")
        todo_list.complete_task(2)
        file_path = tmp_path / "todos.json"
        todo_list.save(file_path)

        loaded = TodoList.load(file_path)
        tasks = loaded.list_tasks()
        assert len(tasks) == 2
        assert tasks[0].title == "Task 1"
        assert tasks[0].completed is False
        assert tasks[1].title == "Task 2"
        assert tasks[1].completed is True

    def test_load_preserves_next_id(self, tmp_path):
        todo_list = TodoList()
        todo_list.add_task("Task 1")
        todo_list.add_task("Task 2")
        file_path = tmp_path / "todos.json"
        todo_list.save(file_path)

        loaded = TodoList.load(file_path)
        new_task = loaded.add_task("Task 3")
        assert new_task.id == 3
