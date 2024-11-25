from __future__ import annotations

import random

from src.parameters import EvolutionParameters, Parameters
from src.types import Group, Hall, Lecturer, Slot, TimeSlot


class Schedule:
    def __init__(self, parameters: Parameters) -> None:
        self.grid: list[Slot] = []
        self.parameters = parameters

    def __str__(self) -> str:
        return "\n".join([str(slot) for slot in self.grid])

    def get_available_lecturers(self, time_slot: TimeSlot) -> list[Lecturer]:
        """Extract available lecturers for a specific timeslot.

        Parameters
        ----------
        time_slot : TimeSlot
            Time at which lecturer must not have lectures.

        Returns
        -------
        list[Lecturer]
        """
        scheduled_slots = [slot for slot in self.grid if slot.time_slot == time_slot]
        scheduled_lecturers = {
            slot.lecturer for slot in scheduled_slots if slot.lecturer
        }
        return [
            lecturer
            for lecturer in self.parameters.lecturers
            if lecturer not in scheduled_lecturers
        ]

    def get_available_halls(self, time_slot: TimeSlot) -> list[Hall]:
        """Extract available halls for a specific timeslot.

        Parameters
        ----------
        time_slot : TimeSlot
            Time at which hall must not have group.

        Returns
        -------
        list[Hall]
        """
        scheduled_slots = [slot for slot in self.grid if slot.time_slot == time_slot]
        scheduled_halls = {slot.hall for slot in scheduled_slots if slot.hall}
        return [hall for hall in self.parameters.halls if hall not in scheduled_halls]

    def get_available_time_slots(
        self, hall: Hall, lecturer: Lecturer, group: Group
    ) -> list[TimeSlot]:
        """Extract available time slots for a hall, lecturer or
        a group.

        Parameters
        ----------
        hall : Hall
        lecturer : Lecturer
        group : Group

        Returns
        -------
        list[TimeSlot]
        """
        scheduled_slots = [
            slot
            for slot in self.grid
            if slot.hall == hall or slot.lecturer == lecturer or slot.group == group
        ]
        occupied_time_slots = {slot.time_slot for slot in scheduled_slots}
        return [
            time_slot
            for time_slot in self.parameters.time_slots
            if time_slot not in occupied_time_slots
        ]

    def _mutate_hall(self, slot: Slot) -> None:
        """Makes in-place mutation of slot's property `hall`.

        Parameters
        ----------
        slot : Slot
            Slot that needs to be mutated.

        Notes
        -----
        If there is no available halls no mutation is being performed.
        """
        available_halls = self.get_available_halls(slot.time_slot)

        if available_halls:
            slot.hall = random.choice(available_halls)

    def _mutate_lecturer(self, slot: Slot) -> None:
        """Makes in-place mutation of slot's property `lecturer`.

        Parameters
        ----------
        slot : Slot
            Slot that needs to be mutated.

        Notes
        -----
        If there is no available lecturers no mutation is being performed.
        """
        available_lecturers = self.get_available_lecturers(slot.time_slot)

        if available_lecturers:
            slot.lecturer = random.choice(available_lecturers)

    def _mutate_timeslot(self, slot: Slot) -> None:
        """Makes in-place mutation of slot's property `time_slot`.

        Parameters
        ----------
        slot : Slot
            Slot that needs to be mutated.

        Notes
        -----
        If there is no available time slots no mutation is being performed.
        """
        available_time_slots = self.get_available_time_slots(
            slot.hall, slot.lecturer, slot.group
        )

        if available_time_slots:
            slot.time_slot = random.choice(available_time_slots)

    def mutate(self, evolution_params: EvolutionParameters) -> None:
        """Makes a mutation of the shedule based on provided parameters.

        Parameters
        ----------
        evolution_params : EvolutionParameters

        Notes
        -----
        With `mut_prob` for each slot in the grid:
        - With probability `hall_prob` apply mutation `change hall`
        - With probability `lecturer_prob` apply mutation `change lecturer`
        - With probability `time_slot_prob` apply mutation `change time slot`
        """
        for slot in self.grid:
            if random.random() > evolution_params.mut_prob:
                continue

            if random.random() < evolution_params.hall_prob:
                self._mutate_hall(slot=slot)

            if random.random() < evolution_params.lecturer_prob:
                self._mutate_lecturer(slot=slot)

            if random.random() < evolution_params.time_slot_prob:
                self._mutate_timeslot(slot=slot)

    def count_total_windows(self) -> int:
        """Calculates the total number of "windows" (gaps) in the schedule across
        all groups.

        Returns
        -------
        int
            The total count of windows across all groups.
        """
        total_windows = 0

        for group in self.parameters.groups:
            group_windows = 0
            group_slots = [slot for slot in self.grid if slot.group == group]

            slots_by_day = {}
            for slot in group_slots:
                if slot.time_slot.day not in slots_by_day:
                    slots_by_day[slot.time_slot.day] = []
                slots_by_day[slot.time_slot.day].append(slot)

            for _, slots in slots_by_day.items():
                sorted_slots = sorted(slots, key=lambda s: s.time_slot.time)

                for i in range(len(sorted_slots) - 1):
                    current_lesson = sorted_slots[i].time_slot.time
                    next_lesson = sorted_slots[i + 1].time_slot.time

                    gap = next_lesson - current_lesson - 1
                    if gap > 0:
                        group_windows += gap

            total_windows += group_windows

        return total_windows

    def count_total_lecturer_windows(self) -> int:
        """Calculates the total number of "windows" (gaps) in the schedule
        across all lecturers.

        Returns
        -------
        int
            The total count of windows across all lecturers.
        """
        total_windows = 0

        for lecturer in self.parameters.lecturers:
            lecturer_windows = 0
            lecturer_slots = [slot for slot in self.grid if slot.lecturer == lecturer]

            slots_by_day = {}
            for slot in lecturer_slots:
                if slot.time_slot.day not in slots_by_day:
                    slots_by_day[slot.time_slot.day] = []
                slots_by_day[slot.time_slot.day].append(slot)

            for _, slots in slots_by_day.items():
                sorted_slots = sorted(slots, key=lambda s: s.time_slot.time)

                for i in range(len(sorted_slots) - 1):
                    current_lesson = sorted_slots[i].time_slot.time
                    next_lesson = sorted_slots[i + 1].time_slot.time

                    gap = next_lesson - current_lesson - 1
                    if gap > 0:
                        lecturer_windows += gap

            total_windows += lecturer_windows

        return total_windows

    def count_total_non_profile_slots(self) -> int:
        """Calculates the total number of slots across all lecturers where they are
        teaching a non-profile subject.

        Returns
        -------
        int
            The total count of non-profile slots across all lecturers.
        """
        total_non_profile_slots = 0

        for slot in self.grid:
            lecturer = slot.lecturer
            if lecturer and slot.subject.name not in lecturer.can_teach_subjects_names:
                total_non_profile_slots += 1

        return total_non_profile_slots

    def count_capacity_overflows(self) -> float:
        """Calculates the total capacity overflow penalty for halls where the group size
        exceeds hall capacity.

        Returns
        -------
        float
            The sum of overflow percentages for all cases where a hall's
            capacity is exceeded.
        """
        total_overflow_penalty = 0.0

        for slot in self.grid:
            group_size = slot.group.capacity
            hall_capacity = slot.hall.capacity

            if group_size > hall_capacity:
                overflow_percentage = (group_size - hall_capacity) / hall_capacity
                total_overflow_penalty += overflow_percentage

        return total_overflow_penalty

    @classmethod
    def create_basic_schedule(cls, parameters: Parameters) -> Schedule:
        """Creates a simple schedule that satisfies the hard constraints:
        - One lecturer can conduct one lesson at a time in one hall with one group.
        - One group can have one lesson at a time.
        - One hall can contain only one lesson at a time.

        Parameters
        ----------
        parameters : Parameters
            The parameters required to generate the schedule.

        Returns
        -------
        Schedule
            A new Schedule object with the grid populated.
        """

        schedule = cls(parameters)
        schedule.grid = []

        for group in parameters.groups:
            shuffled_time_slots = iter(
                random.sample(parameters.time_slots, len(parameters.time_slots))
            )

            for subject_name in group.subject_names:
                subject = next(
                    (subj for subj in parameters.subjects if subj.name == subject_name),
                    None,
                )

                if subject is None:
                    continue

                for _ in range(subject.hours):
                    while True:
                        try:
                            time_slot = next(shuffled_time_slots)

                            available_halls = [
                                hall
                                for hall in parameters.halls
                                if hall
                                not in [
                                    slot.hall
                                    for slot in schedule.grid
                                    if slot.time_slot == time_slot
                                ]
                            ]

                            if not available_halls:
                                continue

                            hall = random.choice(available_halls)

                            # Get available lecturers at this time slot
                            available_lecturers = [
                                lecturer
                                for lecturer in parameters.lecturers
                                if lecturer
                                not in [
                                    slot.lecturer
                                    for slot in schedule.grid
                                    if slot.time_slot == time_slot
                                ]
                            ]

                            if not available_lecturers:
                                continue

                            lecturer = random.choice(available_lecturers)

                            slot = Slot(
                                group=group,
                                subject=subject,
                                lecturer=lecturer,
                                hall=hall,
                                time_slot=time_slot,
                            )
                            schedule.grid.append(slot)
                            break

                        except StopIteration:
                            print(
                                "No available time slots for"
                                f" {group.name} and {subject.name}"
                            )
                            break

        return schedule
