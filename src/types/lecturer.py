from __future__ import annotations


class Lecturer:
    def __init__(self, name: str, can_teach_subjects_names: list[str]) -> None:
        self.name: str = name
        self.can_teach_subjects_names: list[str] = can_teach_subjects_names

    def __eq__(self, other: Lecturer) -> bool:
        return not other or self.name == other.name

    def __str__(self) -> str:
        return f"{self.name}"

    def __hash__(self) -> int:
        return hash(self.name)
