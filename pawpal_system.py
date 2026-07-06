from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime
from typing import List, Optional


@dataclass
class Task:
    title: str
    duration_minutes: int
    priority: str = "medium"
    category: str = "general"
    scheduled_time: Optional[datetime] = None
    completed: bool = False

    def mark_complete(self) -> None:
        """Mark this task as completed."""
        pass

    def reschedule(self, scheduled_time: datetime) -> None:
        """Move the task to a new scheduled time."""
        pass

    def update_priority(self, priority: str) -> None:
        """Adjust the task priority."""
        pass


@dataclass
class Pet:
    name: str
    species: str
    age: Optional[int] = None
    preferences: List[str] = field(default_factory=list)
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Add a new task to this pet."""
        pass

    def remove_task(self, title: str) -> None:
        """Remove a task by title."""
        pass

    def update_preferences(self, preferences: List[str]) -> None:
        """Replace the pet's preferences."""
        pass


@dataclass
class Owner:
    name: str
    availability_minutes: int = 240
    preferred_time_window: Optional[str] = None
    pets: List[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to the owner's profile."""
        pass

    def remove_pet(self, name: str) -> None:
        """Remove a pet by name."""
        pass

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
        pass

    def sort_tasks(self) -> None:
        """Sort tasks based on priority and duration."""
        pass

    def generate_schedule(self) -> List[Task]:
        """Create the ordered task list for the day."""
        return []

    def explain_plan(self) -> str:
        """Return a plain-language explanation of the plan."""
        return ""
