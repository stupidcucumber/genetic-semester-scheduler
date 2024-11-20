import yaml

from src.schedule import Schedule


def save_schedule_to_yaml_student(schedule: Schedule, file_path: str) -> None:
    """
    Saves the given Schedule to a YAML file with lessons sorted by time
    slots for each group.

    :param schedule: The Schedule object to save
    :param file_path: Path to the output YAML file
    """
    schedule_data = {}

    for group in schedule.parameters.groups:
        group_lessons = [slot for slot in schedule.grid if slot.group == group]

        sorted_lessons = sorted(
            group_lessons, key=lambda slot: (slot.time_slot.day, slot.time_slot.time)
        )

        group_lessons_data = []
        for lesson in sorted_lessons:
            lesson_data = {
                "subject": lesson.subject.name,
                "lecturer": lesson.lecturer.name,
                "hall": lesson.hall.name,
                "time_slot": str(lesson.time_slot),
            }
            group_lessons_data.append(lesson_data)

        schedule_data[group.name] = group_lessons_data

    with open(file_path, "w") as file:
        yaml.dump(schedule_data, file, default_flow_style=False, allow_unicode=True)


def save_schedule_to_yaml_lecturer(schedule: Schedule, file_path: str) -> None:
    """
    Saves the given Schedule to a YAML file with lessons sorted by time slots
    for each lecturer.

    :param schedule: The Schedule object to save
    :param file_path: Path to the output YAML file
    """
    schedule_data = {}

    for lecturer in schedule.parameters.lecturers:
        lecturer_lessons = [slot for slot in schedule.grid if slot.lecturer == lecturer]

        sorted_lessons = sorted(
            lecturer_lessons, key=lambda slot: (slot.time_slot.day, slot.time_slot.time)
        )

        lecturer_lessons_data = []
        for lesson in sorted_lessons:
            lesson_data = {
                "group": lesson.group.name,
                "subject": lesson.subject.name,
                "hall": lesson.hall.name,
                "time_slot": str(lesson.time_slot),
            }
            lecturer_lessons_data.append(lesson_data)

        schedule_data[lecturer.name] = lecturer_lessons_data

    with open(file_path, "w") as file:
        yaml.dump(schedule_data, file, default_flow_style=False, allow_unicode=True)


def save_schedule_to_yaml_hall(schedule: Schedule, file_path: str) -> None:
    """
    Saves the given Schedule to a YAML file with lessons sorted by time slots
    for each hall.

    :param schedule: The Schedule object to save
    :param file_path: Path to the output YAML file
    """
    schedule_data = {}

    for hall in schedule.parameters.halls:
        hall_lessons = [slot for slot in schedule.grid if slot.hall == hall]

        sorted_lessons = sorted(
            hall_lessons, key=lambda slot: (slot.time_slot.day, slot.time_slot.time)
        )

        hall_lessons_data = []
        for lesson in sorted_lessons:
            lesson_data = {
                "group": lesson.group.name,
                "subject": lesson.subject.name,
                "lecturer": lesson.lecturer.name,
                "time_slot": str(lesson.time_slot),
            }
            hall_lessons_data.append(lesson_data)

        schedule_data[hall.name] = hall_lessons_data

    with open(file_path, "w") as file:
        yaml.dump(schedule_data, file, default_flow_style=False, allow_unicode=True)


def save_results(schedule: Schedule) -> None:
    save_schedule_to_yaml_student(schedule, "final_students_schedule.yaml")
    save_schedule_to_yaml_lecturer(schedule, "final_lecturers_schedule.yaml")
    save_schedule_to_yaml_hall(schedule, "final_halls_schedule.yaml")
