from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime, timedelta
from typing import List, Optional


@dataclass
class Task:
    title: str
    duration_minutes: int
    priority: str = "medium"
    category: str = "general"
    scheduled_time: Optional[datetime] = None
    completed: bool = False
    pet: Optional["Pet"] = None

    def mark_complete(self) -> None:
        """Mark this task as completed."""
        self.completed = True

    def reschedule(self, scheduled_time: datetime) -> None:
        """Move the task to a new scheduled time."""
        self.scheduled_time = scheduled_time

    def update_priority(self, priority: str) -> None:
        """Adjust the task priority."""
        self.priority = priority


@dataclass
class Pet:
    name: str
    species: str
    age: Optional[int] = None
    preferences: List[str] = field(default_factory=list)
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Add a new task to this pet."""
        task.pet = self
        self.tasks.append(task)

    def remove_task(self, title: str) -> None:
        """Remove a task by title."""
        for i, t in enumerate(self.tasks):
            if t.title == title:
                self.tasks.pop(i)
                t.pet = None
                return
        raise ValueError(f"Task with title '{title}' not found")

    def update_preferences(self, preferences: List[str]) -> None:
        """Replace the pet's preferences."""
        self.preferences = preferences


@dataclass
class Owner:
    name: str
    availability_minutes: int = 240
    preferred_time_window: Optional[str] = None
    pets: List[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to the owner's profile."""
        self.pets.append(pet)

    def remove_pet(self, name: str) -> None:
        """Remove a pet by name."""
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
        """Add a task to the day's plan."""
        self.tasks.append(task)

    def sort_tasks(self) -> None:
        """Sort tasks based on priority and duration."""
        priority_rank = {"high": 3, "medium": 2, "low": 1}
        self.tasks.sort(key=lambda t: (-priority_rank.get(t.priority, 2), t.duration_minutes))

    def generate_schedule(self) -> List[Task]:
        """Create the ordered task list for the day."""
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
