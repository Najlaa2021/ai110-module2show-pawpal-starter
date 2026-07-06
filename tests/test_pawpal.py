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


def test_find_next_available_slot_returns_earliest_time():
    owner = Owner(name="Test", availability_minutes=120)
    pet = Pet(name="Mochi", species="dog")
    owner.add_pet(pet)
    task1 = Task(title="Feeding", duration_minutes=30, scheduled_time=datetime(2026, 1, 1, 8, 30))
    task2 = Task(title="Grooming", duration_minutes=20, scheduled_time=datetime(2026, 1, 1, 9, 15))
    pet.add_task(task1)
    pet.add_task(task2)
    scheduler = Scheduler(owner)

    next_slot = scheduler.find_next_available_slot(15, after=datetime(2026, 1, 1, 8, 0))
    assert next_slot == datetime(2026, 1, 1, 8, 0)


def test_owner_save_and_load_json(tmp_path):
    owner = Owner(name="Jordan", availability_minutes=180)
    pet = Pet(name="Biscuit", species="cat")
    owner.add_pet(pet)
    task = Task(title="Meds", duration_minutes=5, priority="high", scheduled_time=datetime(2026, 1, 1, 10, 0))
    pet.add_task(task)
    file_path = tmp_path / "owner_data.json"

    owner.save_to_json(str(file_path))
    loaded_owner = Owner.load_from_json(str(file_path))

    assert loaded_owner.name == "Jordan"
    assert len(loaded_owner.pets) == 1
    assert loaded_owner.pets[0].name == "Biscuit"
    assert len(loaded_owner.pets[0].tasks) == 1
    assert loaded_owner.pets[0].tasks[0].title == "Meds"


def test_sort_by_time_returns_chronological_order():
    scheduler = Scheduler(Owner(name="Test"))
    first = Task(title="Morning walk", duration_minutes=30, scheduled_time=datetime(2026, 1, 1, 9, 0))
    second = Task(title="Feeding", duration_minutes=10, scheduled_time=datetime(2026, 1, 1, 8, 0))
    third = Task(title="Grooming", duration_minutes=20, scheduled_time=datetime(2026, 1, 1, 10, 30))

    ordered = scheduler.sort_by_time([first, second, third])

    assert [task.title for task in ordered] == ["Feeding", "Morning walk", "Grooming"]


def test_marking_daily_task_creates_next_day_task():
    task = Task(title="Daily meds", duration_minutes=5, frequency="daily")
    today = date(2026, 7, 5)

    next_task = task.mark_complete_and_schedule_next(today)

    assert next_task is not None
    assert next_task.title == "Daily meds"
    assert next_task.completed is False
    assert next_task.scheduled_time == datetime(2026, 7, 6, 0, 0)


def test_detect_conflicts_flags_duplicate_times():
    scheduler = Scheduler(Owner(name="Test"))
    first = Task(title="Feeding", duration_minutes=10, scheduled_time=datetime(2026, 1, 1, 8, 30))
    second = Task(title="Grooming", duration_minutes=20, scheduled_time=datetime(2026, 1, 1, 8, 30))

    warnings = scheduler.detect_conflicts([first, second])

    assert len(warnings) == 1
    assert "Conflict" in warnings[0]
    assert "Feeding" in warnings[0]
    assert "Grooming" in warnings[0]


def test_schedule_assigns_times_by_priority():
    owner = Owner(name="Test")
    pet = Pet(name="Mochi", species="dog")
    owner.add_pet(pet)

    pet.add_task(Task(title="Low priority", duration_minutes=10, priority="low"))
    pet.add_task(Task(title="High priority", duration_minutes=10, priority="high"))

    scheduler = Scheduler(owner)
    scheduled = scheduler.schedule(date(2026, 1, 2))

    assert [task.title for task in scheduled] == ["High priority", "Low priority"]
    assert scheduled[0].scheduled_time == datetime(2026, 1, 2, 8, 0)
    assert scheduled[1].scheduled_time == datetime(2026, 1, 2, 8, 10)


def test_pet_remove_task():
    pet = Pet(name="TestPet", species="dog")
    task = Task(title="Feed", duration_minutes=10)
    pet.add_task(task)
    pet.remove_task("Feed")

    assert len(pet.tasks) == 0
