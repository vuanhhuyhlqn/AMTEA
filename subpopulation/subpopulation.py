from typing import List
from solver import Solver
from indi import Individual
from task import AbstractTask
import numpy as np

class SubPopulation:
    def __init__(self, task: AbstractTask, solver: Solver, lst_indis: List[Individual]):
        self.task = task
        self.solver = solver
        self.lst_indis = lst_indis
        self.size = len(self.lst_indis)

    def get_random_indi(self):
        random_idx = np.random.randint(low=0, high=self.size)
        return self.lst_indis[random_idx]

    def evolve(self):
        lst_offs: List[Individual] = []
        while len(lst_offs) < self.size:
            p1 = self.get_random_indi()
            p2 = self.get_random_indi()
            off : Individual = self.solver([p1, p2])
            off.fitness = self.task.eval(off.gene)

            lst_offs.append(off)
        
        self.lst_indis += lst_offs

        self.lst_indis = sorted(self.lst_indis)
        

        

