import copy
import random
from argparse import ArgumentParser, Namespace
from typing import Callable

from src.genetic import GeneticSchedule
from src.io.yaml import (
    save_schedule_to_yaml_hall,
    save_schedule_to_yaml_lecturer,
    save_schedule_to_yaml_student,
)
from src.parameters import EvolutionParameters
from src.schedule import Schedule

random.seed(0)


def parse_arguments() -> Namespace:
    parser = ArgumentParser()

    parser.add_argument(
        "-c",
        "--config",
        type=str,
        default="assets/config.yaml",
        help="Configuration file that contains info about upcoming schedule.",
    )

    return parser.parse_args()


def generate_selection_function(elitism_ratio: float = 0.1, tournament_size: int = 3):
    """
    Creates a selection function for a population with elitism and tournament
    selection.

    :param elitism_ratio: The ratio of elite individuals to retain
    from the population.
    :param tournament_size: The number of individuals to sample for tournament
    selection.
    :return: A function that returns the selected population.
    """

    def selector(population: list[Schedule], fitness_func: Callable) -> list[Schedule]:
        population.sort(key=fitness_func, reverse=True)

        elitism_count = int(elitism_ratio * len(population))
        new_population = population[:elitism_count]

        while len(new_population) < len(population):
            tournament = random.sample(population, tournament_size)
            tournament.sort(key=fitness_func, reverse=True)
            new_population.append(copy.deepcopy(tournament[0]))

        return new_population

    return selector


def create_fittest_selector():
    """
    Creates a selection function that selects the fittest individual and replicates it
    to generate the entire new population.

    :return: A function that returns a new population containing only copies
    of the fittest individual.
    """

    def selector(population: list[Schedule], fitness_func: callable) -> list[Schedule]:
        population.sort(key=fitness_func, reverse=True)

        fittest_individual = population[0]

        new_population = [
            copy.deepcopy(fittest_individual) for _ in range(len(population))
        ]

        return new_population

    return selector


def generate_fitness_function(
    group_window_weight: float,
    lecturer_window_weight: float,
    non_profile_slot_weight: float,
    capacity_overflow_weight: float,
    distribution_penalty_weight: float = 0,
):
    def fitness(schedule: Schedule) -> float:
        total_group_windows = schedule.count_total_windows()
        total_lecturer_windows = schedule.count_total_lecturer_windows()
        total_non_profile_slots = schedule.count_total_non_profile_slots()
        total_capacity_overflow = schedule.count_capacity_overflows()

        # Distribution of lessons across time slots
        time_slot_counts = dict.fromkeys(schedule.parameters.time_slots, 0)

        for slot in schedule.grid:
            time_slot_counts[slot.time_slot] += 1

        lesson_counts = list(time_slot_counts.values())
        max_count = max(lesson_counts)
        min_count = min(lesson_counts)

        distribution_penalty = max_count - min_count

        fitness_score = (
            group_window_weight * total_group_windows
            + lecturer_window_weight * total_lecturer_windows
            + non_profile_slot_weight * total_non_profile_slots
            + capacity_overflow_weight * total_capacity_overflow
            + distribution_penalty_weight * distribution_penalty
        ) / (
            group_window_weight
            + lecturer_window_weight
            + non_profile_slot_weight
            + capacity_overflow_weight
            + distribution_penalty_weight
        )

        return -1 * fitness_score  # Minimize penalties for optimization

    return fitness


def main(config: str) -> None:
    genetic_schedule = GeneticSchedule.from_yaml(file_path=config)
    fitness_func = generate_fitness_function(
        group_window_weight=10,
        lecturer_window_weight=7,
        non_profile_slot_weight=5,
        capacity_overflow_weight=20,
        distribution_penalty_weight=0,
    )
    selector_func = create_fittest_selector()

    evolution_parameters = EvolutionParameters(
        population_size=100,
        num_of_generations=50,
        mut_prob=0.1,
        fitness_func=fitness_func,
        selector_func=selector_func,
        hall_prob=0.2,
        lecturer_prob=0.2,
        time_slot_prob=0.2,
    )

    final_schedule = genetic_schedule.evolve(evolution_parameters)

    save_schedule_to_yaml_student(final_schedule, "final_students_schedule.yaml")
    save_schedule_to_yaml_lecturer(final_schedule, "final_lecturers_schedule.yaml")
    save_schedule_to_yaml_hall(final_schedule, "final_halls_schedule.yaml")


if __name__ == "__main__":
    args = parse_arguments()

    try:
        main(**dict(args._get_kwargs()))
    except KeyboardInterrupt:
        print("Process had been interrupted by the user.")
    else:
        print("Schedule had been generated.")
