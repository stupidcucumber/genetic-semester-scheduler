from typing import Callable


class EvolutionParameters:
    def __init__(
        self,
        population_size: int,
        num_of_generations: int,
        mut_prob: float,
        fitness_func: Callable,
        selector_func: Callable,
        hall_prob: float,
        lecturer_prob: float,
        time_slot_prob: float,
    ) -> None:
        self.population_size = population_size
        self.num_of_generations = num_of_generations
        self.mut_prob = mut_prob
        self.fitness_func = fitness_func
        self.selector_func = selector_func
        self.hall_prob = hall_prob
        self.lecturer_prob = lecturer_prob
        self.time_slot_prob = time_slot_prob
