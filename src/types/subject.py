from __future__ import annotations


class Subject:
    def __init__(self, name: str, hours: int) -> None:
        self.name: str = name
        self.hours: int = hours

    def __eq__(self, other: Subject) -> bool:
        return not other or self.name == other.name and self.hours == other.hours

    def __str__(self) -> str:
        return f"{self.name}"

    def __hash__(self) -> int:
        return hash((self.name, self.hours))
