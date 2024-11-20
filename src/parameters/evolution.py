from dataclasses import dataclass
from typing import Callable


@dataclass
class EvolutionParameters:
    population_size: int
    num_of_generations: int
    mut_prob: float
    hall_prob: float
    lecturer_prob: float
    time_slot_prob: float
    fitness_func: Callable
    selector_func: Callable
