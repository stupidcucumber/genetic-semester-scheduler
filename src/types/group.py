from __future__ import annotations

from src.types.subject import Subject


class Group:
    def __init__(self, name: str, capacity: int, subject_names: list[str]) -> None:
        self.name: str = name
        self.capacity: int = capacity
        self.subject_names: list[str] = subject_names
        self.subjects: list[Subject] = None

    def __eq__(self, other: Group) -> bool:
        return not other or all(
            [self.name == other.name, self.capacity == other.capacity]
        )

    def __str__(self) -> str:
        return f"{self.name}"

    def __hash__(self) -> int:
        return hash((self.name, self.capacity))
