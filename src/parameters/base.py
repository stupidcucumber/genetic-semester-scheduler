from dataclasses import dataclass

from src.types import Group, Hall, Lecturer, Subject, TimeSlot


@dataclass
class Parameters:
    time_slots: list[TimeSlot]
    subjects: list[Subject]
    groups: list[Group]
    lecturers: list[Lecturer]
    halls: list[Hall]
