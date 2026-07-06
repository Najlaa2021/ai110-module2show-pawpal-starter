import pytest
from pawpal_system import Pet, Task


def test_mark_complete():
    t = Task(title="Test", duration_minutes=5)
    assert not t.completed
    t.mark_complete()
    assert t.completed


def test_add_task_increases_count():
    p = Pet(name="TestPet", species="dog")
    assert len(p.tasks) == 0
    t = Task(title="Feed", duration_minutes=10)
    p.add_task(t)
    assert len(p.tasks) == 1
    assert p.tasks[0].title == "Feed"
