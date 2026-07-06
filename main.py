from datetime import date

from pawpal_system import Owner, Pet, Task, Scheduler


def demo():
    owner = Owner(name="Jordan", availability_minutes=180)

    pet1 = Pet(name="Mochi", species="dog", age=4)
    pet2 = Pet(name="Biscuit", species="cat", age=2)

    t1 = Task(title="Morning walk", duration_minutes=30, priority="high")
    t2 = Task(title="Feeding", duration_minutes=10, priority="high")
    t3 = Task(title="Grooming", duration_minutes=20, priority="low")

    pet1.add_task(t1)
    pet1.add_task(t2)
    pet2.add_task(t3)

    owner.add_pet(pet1)
    owner.add_pet(pet2)

    scheduler = Scheduler(owner)
    scheduled = scheduler.schedule(date.today())

    print(f"Today's Schedule for {owner.name} ({date.today()}):")
    for t in scheduled:
        time_str = t.scheduled_time.strftime("%H:%M") if t.scheduled_time else "unscheduled"
        pet_name = t.pet.name if t.pet else "(unknown)"
        print(f"{time_str} — {t.title} for {pet_name} ({t.duration_minutes} min) [priority: {t.priority}]")


if __name__ == "__main__":
    demo()
