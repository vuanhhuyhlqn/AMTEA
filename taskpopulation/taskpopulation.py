from typing import List, Dict, Optional
import random
import time
import statistics
from task import AbstractTask
from subpopulation import SubPopulation
from indi import Individual
from solver import Solver
from memory import Memory
import numpy as np

class TaskPopulation:
    def __init__(self, task : AbstractTask, size : int, memory_size : int, dim : int):
        # print('Task Population Initiation!')
        self.task = task
        self.size = size
        self.lst_solvers = []
        self.num_solvers = None
        self.mem = Memory(memory_size=memory_size)
        self.dim = dim # Individual dimension
        self.lst_indis : List[Individual] = []
        while not self.is_full():
            i = Individual(dim=self.dim, task_name=self.task.task_name)
            i.fitness = self.task.eval(i.gene)
            self.lst_indis.append(i)
            
        self.good_solvers_history = []
        self.worst_solvers_history = []
        self.best_fitness_hitory = []

    def evolve(self, gen : int, parents : List[Individual]):
        print(f'Task name: {self.task.task_name}')
        print(f'List solvers: {[solver.id for solver in self.lst_solvers]}')

        random.shuffle(self.lst_indis)

        dict_subpopulations : Dict[str, SubPopulation] = {}
        lst_p_values : List[float] = []
        solver_ids : List[str] = [solver.id for solver in self.lst_solvers]

        for solver in self.lst_solvers:
            dict_subpopulations[solver.id] = SubPopulation(self.task, solver)
            lst_p_values.append(self.mem.get_p_value(solver_id=solver.id))

        print(f'[*] lst_p_values: {lst_p_values}')

        for indi in parents:
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
            
            self.mem.set_value(solver_id=solver_id, 
                               generation=gen, 
                               num_success=success, 
                               num_failure=failure)

        # Selection
        self.lst_indis.extend(lst_offs)
        self.lst_indis = sorted(self.lst_indis, key=lambda ind : ind.fitness)
        self.lst_indis = self.lst_indis[:self.size]
        random.shuffle(self.lst_indis)

        for indi in self.lst_indis:
            try:
                assert(indi.task_name == self.task.task_name)
            except:
                print('Indi task name not match!')
        # end = time.time()
        # print(f"Task Subpopulation evolve time taken: {end - start}")

    def get_median_fitness(self) -> float:
        fitness_values = [indi.fitness for indi in self.lst_indis]
        return statistics.median(fitness_values)

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
    
    def compute_pdi(self, window: int = 5,
                    k_sigmoid: float = 1.0,
                    alpha: float = 0.6,
                    gamma: float = 1.5,
                    eps: float = 1e-12):
        
        pop = [indi.gene for indi in self.lst_indis]
        pop_mat = np.vstack([np.asarray(x, dtype=float) for x in pop])
        N, d = pop_mat.shape 
        avg_dist = self.pairwise_avg_distance(pop_mat)
        baseline_diversity = np.sqrt(d) / 3.0 + eps
        
        # Diversity Index: Mức đa dạng -> Đo khả năng explore
        DI = avg_dist / (baseline_diversity + eps)

        DIc = float(np.clip(DI / gamma, 0.0, 1.0))
        
        # Improvement Rate: Mức độ cải thiện fitness
        IR = 0.5
        if self.best_fitness_hitory is not None and len(self.best_fitness_hitory) >= 2:
            print(f'Best fitness history: {self.best_fitness_hitory}')
            L = len(self.best_fitness_hitory)
            w = int(min(window, max(1, L//2)))
            if L >= 2 * w:
                recent = float(np.mean(self.best_fitness_hitory[-w:]))
                past = float(np.mean(self.best_fitness_hitory[-2 * w:-w]))
                raw_improve = past - recent
                print(f'Raw improve: {raw_improve}')
            else:  
                raw_improve = self.best_fitness_hitory[0] - self.best_fitness_hitory[1]
            IR = 1.0 / (1.0 + np.exp(-k_sigmoid * raw_improve))
            print(f'IR before clip: {IR}')
            IR = float(np.clip(IR, 0.0, 1.0))
            print(f'IR after clip: {IR}')

        pdi = alpha * IR + (1.0 - alpha) * DIc
        pdi = float(np.clip(pdi, 0.0, 1.0))
        
        return pdi, IR, DIc

    

        


        