from dataclasses import dataclass, field
from typing import List


@dataclass
class CareTask:
    title: str
    duration_minutes: int
    priority: str  # "low", "medium", "high"
    reason: str = ""

    def is_feasible(self, available_minutes: int) -> bool:
        pass


@dataclass
class Pet:
    name: str
    species: str
    age: int
    tasks: List[CareTask] = field(default_factory=list)

    def add_task(self, task: CareTask) -> None:
        pass

    def get_tasks(self) -> List[CareTask]:
        pass


class Schedule:
    def __init__(self) -> None:
        self.planned_tasks: List[CareTask] = []
        self.total_minutes: int = 0

    def add_task(self, task: CareTask) -> None:
        pass

    def explain(self) -> str:
        pass

    def display(self) -> str:
        pass


class Owner:
    def __init__(self, name: str, available_minutes: int, preferences: str = "") -> None:
        self.name = name
        self.available_minutes = available_minutes
        self.preferences = preferences
        self.pets: List[Pet] = []

    def add_pet(self, pet: Pet) -> None:
        pass

    def get_schedule(self) -> Schedule:
        pass
