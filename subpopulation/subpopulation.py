from typing import List
from ..solver.solver import Solver
from ..indi.indi import Individual


class SubPopulation:
    def __init__(self, solver: Solver, lst_indis: List[Individual]):
        self.solver = solver
        self.lst_indis = lst_indis

    