from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime, timedelta
from typing import List, Optional


def _time_to_minutes(value: Optional[str]) -> int:
    """Convert an HH:MM string into minutes since midnight."""
    if not value:
        return 0
    try:
        hour_str, minute_str = value.split(":")
        return int(hour_str) * 60 + int(minute_str)
    except ValueError:
        return 0


@dataclass
class Task:
    title: str
    duration_minutes: int
    priority: str = "medium"
    category: str = "general"
    description: Optional[str] = None
    frequency: Optional[str] = None
    scheduled_time: Optional[datetime] = None
    completed: bool = False
    pet: Optional["Pet"] = None

    def mark_complete(self) -> None:
        """Mark the task completed."""
        self.completed = True

    def mark_complete_and_schedule_next(self, today: date) -> Optional["Task"]:
        """Advance a recurring task to the next occurrence."""
        self.mark_complete()
        if not self.frequency:
            return None
        next_due = None
        if self.frequency.lower() == "daily":
            next_due = today + timedelta(days=1)
        elif self.frequency.lower() == "weekly":
            next_due = today + timedelta(days=7)
        if next_due is None:
            return None
        return Task(
            title=self.title,
            duration_minutes=self.duration_minutes,
            priority=self.priority,
            category=self.category,
            description=self.description,
            frequency=self.frequency,
            scheduled_time=datetime.combine(next_due, datetime.min.time()),
            completed=False,
            pet=self.pet,
        )

    def reschedule(self, scheduled_time: datetime) -> None:
        """Set a new scheduled time for the task."""
        self.scheduled_time = scheduled_time

    def update_priority(self, priority: str) -> None:
        """Update the task's priority level."""
        self.priority = priority


@dataclass
class Pet:
    name: str
    species: str
    age: Optional[int] = None
    preferences: List[str] = field(default_factory=list)
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Add a Task to this pet and set ownership."""
        task.pet = self
        self.tasks.append(task)

    def remove_task(self, title: str) -> None:
        """Remove a Task by its title."""
        for i, t in enumerate(self.tasks):
            if t.title == title:
                self.tasks.pop(i)
                t.pet = None
                return
        raise ValueError(f"Task with title '{title}' not found")

    def update_preferences(self, preferences: List[str]) -> None:
        """Replace this pet's preference list."""
        self.preferences = preferences


@dataclass
class Owner:
    name: str
    availability_minutes: int = 240
    preferred_time_window: Optional[str] = None
    pets: List[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """Add a Pet to the owner's list."""
        self.pets.append(pet)

    def remove_pet(self, name: str) -> None:
        """Remove a Pet by name."""
        for i, p in enumerate(self.pets):
            if p.name == name:
                self.pets.pop(i)
                return
        raise ValueError(f"Pet with name '{name}' not found")

    def create_daily_plan(self, plan_date: date) -> "DailyPlan":
        """Create a day plan for this owner."""
        return DailyPlan(owner=self, date=plan_date)


@dataclass
class DailyPlan:
    owner: Owner
    date: date
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Add a Task to this DailyPlan."""
        self.tasks.append(task)

    def sort_tasks(self) -> None:
        """Sort tasks by priority (high→low) then by duration (shorter first)."""
        priority_rank = {"high": 3, "medium": 2, "low": 1}
        self.tasks.sort(key=lambda t: (-priority_rank.get(t.priority, 2), t.duration_minutes))

    def generate_schedule(self) -> List[Task]:
        """Assemble and schedule tasks sequentially within owner's availability."""
        # If no tasks were explicitly added to the plan, collect all tasks from the owner's pets
        if not self.tasks:
            for pet in self.owner.pets:
                for t in pet.tasks:
                    self.tasks.append(t)

        self.sort_tasks()

        # Schedule sequentially starting at 08:00 local time
        start_hour = 8
        current = datetime(self.date.year, self.date.month, self.date.day, start_hour, 0)
        remaining = self.owner.availability_minutes
        scheduled: List[Task] = []

        for task in list(self.tasks):
            if task.duration_minutes <= remaining:
                task.scheduled_time = current
                current = current + timedelta(minutes=task.duration_minutes)
                remaining -= task.duration_minutes
                scheduled.append(task)

        # Replace tasks with only the scheduled subset
        self.tasks = scheduled
        return scheduled

    def explain_plan(self) -> str:
        """Return a plain-language explanation of the plan."""
        if not self.tasks:
            return "No tasks scheduled. Call `generate_schedule()` first."

        lines: List[str] = []
        for t in self.tasks:
            time_str = t.scheduled_time.strftime("%H:%M") if t.scheduled_time else "unscheduled"
            lines.append(f"{time_str} — {t.title} ({t.duration_minutes} min) [priority: {t.priority}]")

        return "\n".join(lines)


class Scheduler:
    """The scheduler coordinates owners, pets, and daily plans."""

    def __init__(self, owner: Owner):
        """Create a scheduler for an owner."""
        self.owner = owner

    def collect_tasks(self) -> List[Task]:
        """Return all tasks across the owner's pets."""
        tasks: List[Task] = []
        for pet in self.owner.pets:
            tasks.extend(pet.tasks)
        return tasks

    def build_plan(self, plan_date: date) -> DailyPlan:
        """Create a DailyPlan for the given date using owner's tasks."""
        plan = DailyPlan(owner=self.owner, date=plan_date)
        for t in self.collect_tasks():
            plan.add_task(t)
        return plan

    def schedule(self, plan_date: date) -> List[Task]:
        """Generate and return the scheduled tasks for the date."""
        plan = self.build_plan(plan_date)
        return plan.generate_schedule()

    def sort_by_time(self, tasks: List[Task]) -> List[Task]:
        """Sort tasks by their scheduled time, falling back to title order."""
        return sorted(
            tasks,
            key=lambda task: (
                task.scheduled_time.time().hour * 60 + task.scheduled_time.time().minute
                if task.scheduled_time
                else 24 * 60,
                task.title,
            ),
        )

    def filter_tasks(self, tasks: List[Task], pet_name: Optional[str] = None, completed: Optional[bool] = None) -> List[Task]:
        """Filter tasks by pet name and/or completion status."""
        filtered = list(tasks)
        if pet_name:
            filtered = [task for task in filtered if task.pet and task.pet.name.lower() == pet_name.lower()]
        if completed is not None:
            filtered = [task for task in filtered if task.completed is completed]
        return filtered

    def detect_conflicts(self, tasks: List[Task]) -> List[str]:
        """Return lightweight warnings for tasks that share the same scheduled time."""
        warnings: List[str] = []
        seen = {}
        for task in tasks:
            if task.scheduled_time is None:
                continue
            key = task.scheduled_time.strftime("%H:%M")
            if key in seen:
                warnings.append(
                    f"Conflict: {seen[key].title} and {task.title} are both scheduled at {key}."
                )
            else:
                seen[key] = task
        return warnings

