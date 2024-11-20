from __future__ import annotations


class Hall:
    def __init__(self, name, capacity):
        self.name = name
        self.capacity = capacity

    def __eq__(self, other: Hall) -> bool:
        return not other or self.name == other.name and self.capacity == other.capacity

    def __str__(self) -> str:
        return f"{self.name}"

    def __hash__(self) -> int:
        return hash((self.name, self.capacity))
