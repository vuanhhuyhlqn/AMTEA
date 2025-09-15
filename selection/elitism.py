from .abstract import AbstractSelection
from typing import List
from indi import Individual

class ElitismSelection(AbstractSelection):
    def __init__(self, size):
        self.size = size
    
    def __call__(self, lst_indis: List[Individual]) -> List[Individual]:
        lst_indis = sorted(lst_indis, key=lambda indi: indi.fitness)
        return lst_indis[:self.size]