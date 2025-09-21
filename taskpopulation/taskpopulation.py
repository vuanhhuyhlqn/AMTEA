from typing import List, Dict, Optional, Tuple
import random
import time
import statistics
from task import AbstractTask
from subpopulation import SubPopulation
from indi import Individual
from solver import Solver
from new_memory import Memory, Record
from selection import *
import numpy as np
import math

class TaskPopulation:
    def __init__(self, task : AbstractTask, size : int, memory_size : int, dim : int):
        # print('Task Population Initiation!')
        self.task = task
        self.size = size
        self.lst_solvers : List[Solver] = []
        self.num_solvers = None
        self.mem = Memory(memory_size=memory_size)
        self.record = Record()

        self.dim = dim # Individual dimension
        self.lst_indis : List[Individual] = []
        while not self.is_full():
            i = Individual(dim=self.dim, task_name=self.task.task_name)
            i.fitness = self.task.eval(i.gene)
            self.lst_indis.append(i)
        
        self.good_solvers_history = []
        self.worst_solvers_history = []
        self.best_fitness_hitory = []
        self.solver1_subpop_size = 0

    def evolve(self, gen : int, parents : List[Individual]):
        # print(f'Task name: {self.task.task_name}')
        # print(f'List solvers: {[solver.id for solver in self.lst_solvers]}')
        random.shuffle(self.lst_indis)

        dict_subpopulations : Dict[str, SubPopulation] = {}
        solver_ids : List[str] = [solver.id for solver in self.lst_solvers]

        for solver in self.lst_solvers:
            dict_subpopulations[solver.id] = SubPopulation(self.task, solver, self.record)
        
        # print(f'[*] Solver 1 subpopulation size: {self.solver1_subpop_size}')
        dict_subpopulations[self.lst_solvers[0].id].lst_indis = [indi for indi in self.lst_indis[:self.solver1_subpop_size]]
        dict_subpopulations[self.lst_solvers[1].id].lst_indis = [indi for indi in self.lst_indis[self.solver1_subpop_size:]]
        
        if self.lst_solvers[0].id == 'de':
            dict_subpopulations[self.lst_solvers[0].id].selection = TournamentSelection(self.solver1_subpop_size, 3)   
            dict_subpopulations[self.lst_solvers[1].id].selection = ElitismSelection(self.size - self.solver1_subpop_size)
        else:
            dict_subpopulations[self.lst_solvers[1].id].selection = TournamentSelection(self.solver1_subpop_size, 3)   
            dict_subpopulations[self.lst_solvers[0].id].selection = ElitismSelection(self.size - self.solver1_subpop_size)       
        
        cur_median_fitness : float = self.get_median_fitness()

        new_lst_indis : List[Individual] = []
        
        new_lst_indis.extend(dict_subpopulations[self.lst_solvers[0].id].evolve(parents[:self.solver1_subpop_size]))
        new_lst_indis.extend(dict_subpopulations[self.lst_solvers[1].id].evolve(parents[self.solver1_subpop_size:]))

        succ = []
        fail = []
        for solver_id in solver_ids:

            success, failure = dict_subpopulations[solver_id].cal_succ_fail(cur_median_fitness)
            succ.append(success)
            fail.append(failure)
        
        self.mem.add_succ((succ[0], succ[1]))
        self.mem.add_fail((fail[0], fail[1]))
        # print(f'Length of success memory: {len(self.mem.succ)}')
        # print(f'Length of failure memory: {len(self.mem.fail)}')
        self.mem.cal_succ_p()
            
        self.lst_indis = new_lst_indis
        assert(len(self.lst_indis) == self.size)

        for indi in self.lst_indis:
            try:
                assert(indi.task_name == self.task.task_name)
            except:
                print('Indi task name not match!')
        # end = time.time()
        # print(f"Task Subpopulation evolve time taken: {end - start}")

    def get_median_fitness(self) -> float:
        fitness_values = [indi.fitness for indi in self.lst_indis]
        # return np.quantile(fitness_values, 1/4)
        return np.median(fitness_values)

    def get_best_fitness(self) -> float:
        best_fitness = np.inf
        for indi in self.lst_indis:
            if indi.fitness < best_fitness:
                best_fitness = indi.fitness
        self.best_fitness_hitory.append(best_fitness)
        return best_fitness

    def add_individual(self, indi : Individual):
        assert(self.is_full() == False)
        self.lst_indis.append(indi)

    def get_random_individuals(self, k : int) -> List[Individual]:
        random.shuffle(self.lst_indis)
        assert(k < len(self.lst_indis))

        ret : List[Individual] = []
        while len(ret) < k:
            random_id = random.randrange(self.size)
            ret.append(self.lst_indis[random_id])
        return ret

    def remove_individuals(self, k : int) -> List[Individual]:
        random.shuffle(self.lst_indis)
        assert(k < len(self.lst_indis))

        ret = self.lst_indis[-k:]
        self.lst_indis = self.lst_indis[:-k]

        return ret

    def is_full(self) -> bool:
        return len(self.lst_indis) == self.size
    
    def pairwise_avg_distance(self, X: np.ndarray) -> float:
        # Khoảng cách Euclidean trung bình theo từng cặp
        N = X.shape[0]
        if N < 2:
            return 0.0
        diffs = X[:, None, :] - X[None, :, :]
        dists = np.sqrt(np.sum(diffs**2, axis=2))
        iu = np.triu_indices(N, k=1)
        return float(dists[iu].mean())
    

        


        