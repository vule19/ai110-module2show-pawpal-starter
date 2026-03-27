from dataclasses import dataclass, field
from enum import Enum
from typing import List


class Priority(Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3


@dataclass
class CareTask:
    title: str
    duration_minutes: int
    priority: Priority
    reason: str = ""
    completed: bool = False

    def is_feasible(self, available_minutes: int) -> bool:
        """Return True if this task fits within the given number of available minutes."""
        return self.duration_minutes <= available_minutes

    def mark_complete(self) -> None:
        """Mark this task as completed."""
        self.completed = True


@dataclass
class Pet:
    name: str
    species: str
    age: int
    tasks: List[CareTask] = field(default_factory=list)

    def add_task(self, task: CareTask) -> None:
        """Add a care task to this pet's task list."""
        self.tasks.append(task)

    def get_tasks(self) -> List[CareTask]:
        """Return all care tasks assigned to this pet."""
        return self.tasks


class Schedule:
    def __init__(self, available_minutes: int) -> None:
        """Initialize an empty schedule with the owner's total available time budget."""
        self.available_minutes = available_minutes
        self.planned_tasks: List[CareTask] = []
        self.total_minutes: int = 0

    def add_task(self, task: CareTask) -> None:
        """Add a task to the schedule and update the total time used."""
        self.planned_tasks.append(task)
        self.total_minutes += task.duration_minutes

    def explain(self) -> str:
        """Return a string describing each scheduled task with its priority and reason."""
        if not self.planned_tasks:
            return "No tasks were scheduled."
        lines = []
        for task in self.planned_tasks:
            reason = f" ({task.reason})" if task.reason else ""
            lines.append(
                f"- {task.title}: priority={task.priority.name.lower()}, "
                f"{task.duration_minutes} min{reason}"
            )
        lines.append(f"\nTotal time: {self.total_minutes} / {self.available_minutes} min used.")
        return "\n".join(lines)

    def display(self) -> str:
        """Return a numbered, human-readable summary of today's planned tasks."""
        if not self.planned_tasks:
            return "No tasks scheduled for today."
        lines = ["Today's plan:"]
        for i, task in enumerate(self.planned_tasks, start=1):
            lines.append(f"  {i}. {task.title} ({task.duration_minutes} min)")
        lines.append(f"\n{self.total_minutes} of {self.available_minutes} minutes used.")
        return "\n".join(lines)


class Owner:
    def __init__(self, name: str, available_minutes: int, preferences: str = "") -> None:
        """Initialize an owner with their name, daily time budget, and optional preferences."""
        self.name = name
        self.available_minutes = available_minutes
        self.preferences = preferences
        self.pets: List[Pet] = []

    def add_pet(self, pet: Pet) -> None:
        """Register a pet under this owner."""
        self.pets.append(pet)

    def get_all_tasks(self) -> List[CareTask]:
        """Collect and return all care tasks across every pet owned."""
        all_tasks = []
        for pet in self.pets:
            all_tasks.extend(pet.get_tasks())
        return all_tasks

    def get_schedule(self) -> "Schedule":
        """Build and return a daily schedule by greedily fitting tasks highest-priority first."""
        schedule = Schedule(self.available_minutes)
        remaining = self.available_minutes

        # Sort highest priority first; break ties by shortest duration (fits more in)
        tasks = sorted(
            self.get_all_tasks(),
            key=lambda t: (-t.priority.value, t.duration_minutes),
        )

        for task in tasks:
            if task.is_feasible(remaining):
                schedule.add_task(task)
                remaining -= task.duration_minutes

        return schedule
