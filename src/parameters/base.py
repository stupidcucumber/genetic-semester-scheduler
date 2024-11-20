from src.types import Group, Hall, Lecturer, Subject, TimeSlot


class Parameters:
    def __init__(
        self,
        time_slots: list[TimeSlot],
        subjects: list[Subject],
        groups: list[Group],
        lecturers: list[Lecturer],
        halls: list[Hall],
    ):
        self.time_slots: list[TimeSlot] = time_slots
        self.subjects: list[Subject] = subjects
        self.groups: list[Group] = groups
        self.lecturers: list[Lecturer] = lecturers
        self.halls: list[Hall] = halls
