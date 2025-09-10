from typing import List, Dict
import random
import statistics
from task import AbstractTask
from subpopulation import SubPopulation
from indi import Individual
from solver import Solver
from memory import Memory
import numpy as np

class TaskPopulation:
    def __init__(self, task : AbstractTask, size : int, lst_solvers: List[Solver], mem : Memory, dim : int):
        self.task = task
        self.size = size
        self.lst_solvers = lst_solvers
        self.num_solvers = len(self.lst_solvers)
        self.mem = mem
        self.dim = dim # Individual dimension
        self.lst_indis : List[Individual] = []
        while not self.is_full():
            i = Individual(self.dim)
            i.fitness = self.task.eval(i.gene)
            self.lst_indis.append(Individual(self.dim))

    def evolve(self, gen : int):
        # divide lst_indis into subpopulation
        dict_subpopulations : Dict[str, SubPopulation] = {}
        lst_p_values : List[float] = []
        solver_ids : List[str] = [solver.id for solver in self.lst_solvers]


        for solver in self.lst_solvers:
            dict_subpopulations[solver.id] = SubPopulation(self.task, solver)
            lst_p_values.append(self.mem.get_p_value(task_name=self.task.task_name, solver_id=solver.id))

        print(self.task.task_name)
        print(lst_p_values)


        for indi in self.lst_indis:
            chosen_solver_id = random.choices(solver_ids, weights=lst_p_values, k=1)[0]
            dict_subpopulations[chosen_solver_id].add_individual(indi)
        
        cur_median_fitness : float = self.get_median_fitness()

        lst_offs : List[Individual] = []

        for solver_id in solver_ids:
            lst_offs_subpop = dict_subpopulations[solver_id].evolve() # Offsprings from subpopulation's evolution
            lst_offs.extend(lst_offs_subpop)

            success, failure = 0, 0
            for off in lst_offs_subpop:
                if off.fitness < cur_median_fitness:
                    success += 1
                else:
                    failure += 1
            
            self.mem.set_value(task_name=self.task.task_name, 
                               solver_id=solver_id, 
                               generation=gen, 
                               num_success=success, 
                               num_failure=failure)

        # Selection
        self.lst_indis.extend(lst_offs)
        self.lst_indis = sorted(self.lst_indis)
        self.lst_indis = self.lst_indis[:self.size]
        random.shuffle(self.lst_indis)

    def get_median_fitness(self) -> float:
        fitness_values = [indi.fitness for indi in self.lst_indis]
        return statistics.median(fitness_values)

    def get_best_fitness(self) -> float:
        best_fitness = np.inf
        for indi in self.lst_indis:
            if indi.fitness < best_fitness:
                best_fitness = indi.fitness
        return best_fitness

    def add_individual(self, indi : Individual):
        assert(self.is_full() == False)
        self.lst_indis.append(indi)

    def remove_individuals(self, k : int) -> List[Individual]:
        random.shuffle(self.lst_indis)
        assert(k < len(self.lst_indis))

        ret = self.lst_indis[-k:]
        self.lst_indis = self.lst_indis[:-k]
        print(f'Len indis : {len(self.lst_indis)}')
        print(f'Size : {self.size}')
        print(f'Is full : {self.is_full()}')

        return ret

    def is_full(self) -> bool:
        return len(self.lst_indis) == self.size

    def remove_solvers(self, solver_ids):
        pass

    def add_solvers(self, solver_ids):
        pass

    

        


        