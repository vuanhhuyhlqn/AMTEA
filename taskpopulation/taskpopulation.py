from typing import List
from task import AbstractTask
from subpopulation import SubPopulation
from indi import Individual
from solver import Solver

class TaskPopulation:
    def __init__(self, task : AbstractTask, size : int, lst_solvers: List[Solver]):
        self.task = task
        self.size = size
        self.lst_solvers = lst_solvers
        self.num_solvers = len(self.lst_solvers)
        

        self.lst_indis : List[Individual] = []
        while len(self.lst_indis) < self.size:
            self.lst_indis.append(Individual(self.task.dim))

    def evolve(self):
        pass

    def get_median_fitness(self) -> float:
        pass

    def remove_solvers(self, solver_ids):
        pass

    def add_solvers(self, solver_ids):
        pass


        


        