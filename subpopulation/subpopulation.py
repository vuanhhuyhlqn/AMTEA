from typing import List
from solver import Solver
from indi import Individual
from task import AbstractTask
import numpy as np

class SubPopulation:
    def __init__(self, task: AbstractTask, solver: Solver):
        self.task = task
        self.solver = solver
        self.lst_indis : List[Individual] = []

    def add_individual(self, indi : Individual):
        self.lst_indis.append(indi)

    def get_random_indi(self, size: int) -> Individual:
        random_idx = np.random.randint(low=0, high=size)
        return self.lst_indis[random_idx]

    def evolve(self) -> List[Individual]:
        size = len(self.lst_indis)
        lst_offs: List[Individual] = []
        while len(lst_offs) < size:
            p1 = self.get_random_indi(size=size)
            p2 = self.get_random_indi(size=size)
            off : Individual = Individual(dim=p1.dim, gene=self.solver([p1.gene, p2.gene]))
            off.fitness = self.task.eval(off.gene)
            lst_offs.append(off)
        
        return lst_offs
        

        

