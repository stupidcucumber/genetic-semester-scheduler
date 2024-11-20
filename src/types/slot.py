from dataclasses import dataclass

from src.types.group import Group
from src.types.hall import Hall
from src.types.lecturer import Lecturer
from src.types.subject import Subject
from src.types.timeslot import TimeSlot


@dataclass(frozen=True)
class Slot:
    group: Group
    subject: Subject
    lecturer: Lecturer
    hall: Hall
    time_slot: TimeSlot
