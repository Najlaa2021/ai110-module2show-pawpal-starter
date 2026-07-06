from datetime import date, datetime, time

from pawpal_system import Owner, Pet, Scheduler, Task


def demo():
    owner = Owner(name="Jordan", availability_minutes=180)
    pet1 = Pet(name="Mochi", species="dog", age=4)
    pet2 = Pet(name="Biscuit", species="cat", age=2)
    owner.add_pet(pet1)
    owner.add_pet(pet2)

    t1 = Task(title="Morning walk", duration_minutes=30, priority="high", scheduled_time=datetime.combine(date.today(), time(9, 0)))
    t2 = Task(title="Feeding", duration_minutes=10, priority="high", scheduled_time=datetime.combine(date.today(), time(8, 30)))
    t3 = Task(title="Grooming", duration_minutes=20, priority="low", scheduled_time=datetime.combine(date.today(), time(8, 30)))
    t4 = Task(title="Daily meds", duration_minutes=5, priority="medium", frequency="daily", scheduled_time=datetime.combine(date.today(), time(10, 0)))

    pet1.add_task(t1)
    pet1.add_task(t2)
    pet2.add_task(t3)
    pet2.add_task(t4)

    scheduler = Scheduler(owner)
    sorted_tasks = scheduler.sort_by_time([t1, t2, t3, t4])
    pending_for_mochi = scheduler.filter_tasks(sorted_tasks, pet_name="Mochi", completed=False)
    conflicts = scheduler.detect_conflicts(sorted_tasks)

    next_task = t4.mark_complete_and_schedule_next(date.today())
    if next_task is not None:
        pet2.add_task(next_task)

    print("Sorted tasks:")
    for task in sorted_tasks:
        time_str = task.scheduled_time.strftime("%H:%M") if task.scheduled_time else "unscheduled"
        print(f"- {time_str} — {task.title} ({task.duration_minutes} min)")

    print("\nPending tasks for Mochi:")
    for task in pending_for_mochi:
        print(f"- {task.title}")

    print("\nConflicts:")
    if conflicts:
        for warning in conflicts:
            print(f"- {warning}")
    else:
        print("- None")

    print("\nRecurring follow-up:")
    if next_task is not None:
        print(f"- Created {next_task.title} for {pet2.name}")

    print("\nToday's Schedule:")
    for task in scheduler.schedule(date.today()):
        time_str = task.scheduled_time.strftime("%H:%M") if task.scheduled_time else "unscheduled"
        print(f"- {time_str} — {task.title} for {task.pet.name if task.pet else 'unknown'}")


if __name__ == "__main__":
    demo()
