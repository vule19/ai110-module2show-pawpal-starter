@dataclass
class CareTask:
    title: str
    duration_minutes: int
    priority: Priority
    reason: str = ""
    completed: bool = False

    def is_feasible(self, available_minutes: int) -> bool:
        return self.duration_minutes <= available_minutes

    def mark_complete(self) -> None:
        self.completed = True