from __future__ import annotations

import yaml
from prettytable import PrettyTable

from src.parameters import EvolutionParameters, Parameters
from src.schedule import Schedule
from src.types import Group, Hall, Lecturer, Subject, TimeSlot


class GeneticSchedule:
    def __init__(self, parameters: Parameters) -> None:
        self.parameters = parameters

    @classmethod
    def from_yaml(cls, file_path: str) -> GeneticSchedule:
        """Loads YAML file configuration.

        Parameters
        ----------
        file_path : str
            Path to the yaml containing config.
        """
        try:
            with open(file_path, "r") as file:
                data = yaml.load(file, Loader=yaml.FullLoader)

                required_keys = [
                    "time_slots",
                    "subjects",
                    "groups",
                    "lecturers",
                    "halls",
                ]
                for key in required_keys:
                    if key not in data:
                        raise ValueError(f"Missing required key: {key} in YAML file.")

                time_slots = [TimeSlot(**time_slot) for time_slot in data["time_slots"]]
                subjects = [Subject(**subject) for subject in data["subjects"]]
                groups = [Group(**group) for group in data["groups"]]
                lecturers = [Lecturer(**lecturer) for lecturer in data["lecturers"]]
                halls = [Hall(**hall) for hall in data["halls"]]

                parameters = Parameters(time_slots, subjects, groups, lecturers, halls)

                return cls(parameters)

        except FileNotFoundError:
            print(f"Error: File {file_path} not found.")
        except yaml.YAMLError as e:
            print(f"Error parsing YAML file: {e}")
        except ValueError as e:
            print(f"Error: {e}")

    def generate_population(self, size: int) -> list[Schedule]:
        """Generate a population of 'n' schedules using the create_basic_schedule method
        from the Schedule class.

        Parameters
        ----------
        size : int
            The number of schedules to generate.

        Returns
        -------
        list[Schedule]
            A list of generated schedules.
        """
        population = []

        for _ in range(size):
            schedule = Schedule.create_basic_schedule(self.parameters)
            population.append(schedule)

        return population

    def evolve(self, evolution_params: EvolutionParameters) -> Schedule:
        """Evolves a population of schedules to optimize fitness.

        Parameters
        ----------
        evolution_params : EvolutionParameters
            Parameters needed for evolution

        Returns
        -------
        Schedule
            The best fitness after the evolution process.
        """
        population = [
            Schedule.create_basic_schedule(self.parameters)
            for _ in range(evolution_params.population_size)
        ]

        table = PrettyTable()
        table.field_names = [
            "Generation",
            "Best Fitness",
            "Second Best Fitness",
            "Third Best Fitness",
        ]

        for generation in range(evolution_params.num_of_generations):
            for individual in population:
                individual.mutate(evolution_params)

            fitness_scores = [evolution_params.fitness_func(ind) for ind in population]
            top_3_fitness_before_selection = sorted(fitness_scores, reverse=True)[:3]

            table.add_row(
                [
                    generation + 1,
                    (
                        f"{top_3_fitness_before_selection[0]:.2f}"
                        if len(top_3_fitness_before_selection) > 0
                        else "N/A"
                    ),
                    (
                        f"{top_3_fitness_before_selection[1]:.2f}"
                        if len(top_3_fitness_before_selection) > 1
                        else "N/A"
                    ),
                    (
                        f"{top_3_fitness_before_selection[2]:.2f}"
                        if len(top_3_fitness_before_selection) > 2
                        else "N/A"
                    ),
                ]
            )

            print("\033c", end="")  # This clears the console
            print(table)

            population = evolution_params.selector_func(
                population,
                evolution_params.fitness_func,
            )

        best_schedule = max(population, key=evolution_params.fitness_func)
        return best_schedule
