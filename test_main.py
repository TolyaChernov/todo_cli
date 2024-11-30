import os

import pytest

from main import TaskManager


@pytest.fixture
def setup_task_manager():
    filename = "test_tasks.json"
    manager = TaskManager(filename)
    yield manager
    if os.path.exists(filename):
        os.remove(filename)


def test_add_task(setup_task_manager):
    manager = setup_task_manager
    task = manager.add_task(
        "Test task", "Test description", "Work", "2023-12-31", "High"
    )
    assert task.title == "Test task"
    assert len(manager.tasks) == 1


def test_mark_task_completed(setup_task_manager):
    manager = setup_task_manager
    task = manager.add_task(
        "Test task", "Test description", "Work", "2023-12-31", "High"
    )
    manager.mark_task_completed(task.task_id)
    assert manager.get_task(task.task_id).completed is True


def test_delete_task(setup_task_manager):
    manager = setup_task_manager
    task = manager.add_task(
        "Test task", "Test description", "Work", "2023-12-31", "High"
    )
    manager.delete_task(task.task_id)
    assert manager.get_task(task.task_id) is None


def test_search_tasks(setup_task_manager):
    manager = setup_task_manager
    manager.add_task(
        "First task",
        "Test description",
        "Work",
        "2023-12-31",
        "High")
    manager.add_task(
        "Second task", "Another description", "Personal", "2023-11-30", "Medium"
    )

    results = manager.search_tasks(keyword="First")
    assert len(results) == 1

    results = manager.search_tasks(category="Personal")
    assert len(results) == 1
