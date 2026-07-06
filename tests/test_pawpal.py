from datetime import date, datetime

from pawpal_system import Owner, Pet, Scheduler, Task


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


def test_sort_by_time_orders_tasks():
    scheduler = Scheduler(Owner(name="Test"))
    first = Task(title="Later", duration_minutes=15, scheduled_time=datetime(2026, 1, 1, 10, 0))
    second = Task(title="Earlier", duration_minutes=15, scheduled_time=datetime(2026, 1, 1, 8, 0))
    ordered = scheduler.sort_by_time([first, second])
    assert [task.title for task in ordered] == ["Earlier", "Later"]


def test_filter_tasks_by_pet_and_status():
    owner = Owner(name="Test")
    pet = Pet(name="Mochi", species="dog")
    owner.add_pet(pet)
    pending = Task(title="Pending", duration_minutes=10)
    completed = Task(title="Done", duration_minutes=5)
    completed.mark_complete()
    pet.add_task(pending)
    pet.add_task(completed)
    scheduler = Scheduler(owner)
    filtered = scheduler.filter_tasks([pending, completed], pet_name="Mochi", completed=False)
    assert filtered == [pending]


def test_recurring_task_creates_next_occurrence():
    task = Task(title="Daily meds", duration_minutes=5, frequency="daily")
    next_task = task.mark_complete_and_schedule_next(date.today())
    assert next_task is not None
    assert next_task.frequency == "daily"
    assert next_task.completed is False
