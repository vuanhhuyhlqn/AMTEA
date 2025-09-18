from typing import List
import time
from selection import AbstractSelection
from solver import Solver
from indi import Individual
from task import AbstractTask
from selection import AbstractSelection
import numpy as np

class SubPopulation:
    def __init__(self, task: AbstractTask, solver: Solver):
        self.task = task
        self.solver = solver
        self.lst_indis : List[Individual] = []
        self.selection : AbstractSelection = None

    def add_individual(self, indi : Individual):
        self.lst_indis.append(indi)

    def get_random_indi(self, size: int) -> Individual:
        random_idx = np.random.randint(low=0, high=size)
        return self.lst_indis[random_idx]

    def evolve(self, parents: List[Individual]) -> List[Individual]:
        try:
            off_genes = self.solver(np.vstack([indi.gene for indi in parents]))
            off_fitnesses = self.task.batch_eval(off_genes)
            for off_fitness in off_fitnesses:
                if off_fitness == np.inf:
                    raise Exception('[ERROR] Off fitness inf!')

            lst_offs = [Individual(self.task.dim, gene=off_gene, fitness=off_fitness, task_name=self.task.task_name) for off_gene, off_fitness in zip(off_genes, off_fitnesses)]
            self.lst_indis.extend(lst_offs)
            self.lst_indis = self.selection(self.lst_indis)
            return self.lst_indis
        except:
            return self.lst_indis
        
    def cal_succ_fail(self, cur_median_fitness: float):
        succ = 0
        fail = 0
        for indi in self.lst_indis:
            if indi.fitness < cur_median_fitness:
                succ += 1
            else:
                fail += 1
        return succ, fail
        

        

