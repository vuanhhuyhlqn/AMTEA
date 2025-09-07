from typing import List
from solver import Solver
from indi import Individual


class SubPopulation:
    def __init__(self, solver: Solver, lst_indis: List[Individual]):
        self.solver = solver
        self.lst_indis = lst_indis

    def evolve(self):
        pass   