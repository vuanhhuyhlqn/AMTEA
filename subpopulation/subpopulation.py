from typing import List
import time
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
        start = time.time()
        size = len(self.lst_indis)
        lst_offs: List[Individual] = []

        off_genes = self.solver(np.vstack([indi.gene for indi in self.lst_indis]))
        off_fitnesses = self.task.batch_eval(off_genes)
        lst_offs = [Individual(self.task.dim, gene=off_gene, fitness=off_fitness) for off_gene, off_fitness in zip(off_genes, off_fitnesses)]

        end = time.time()
        print(f"Subpopulation evolve time taken: {end - start}")
        return lst_offs
        

        

