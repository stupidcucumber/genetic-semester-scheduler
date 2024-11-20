from __future__ import annotations


class TimeSlot:
    def __init__(self, day: str, time: int) -> None:
        self.day: str = day
        self.time: int = time

    def __eq__(self, other: TimeSlot | None) -> bool:
        return not other or self.day == other.day and self.time == other.time

    def __str__(self) -> str:
        return f"{self.day}, {self.time}"

    def __repr__(self) -> str:
        return f"{self.day}, {self.time}"

    def __hash__(self) -> int:
        return hash((self.day, self.time))
