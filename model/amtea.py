from typing import List, Dict
from .abstract import AbstractModel
from population import Population
from task import AbstractTask
from solver import Solver
from utils.utils import *
from LLM.llm import LLM
from dotenv import load_dotenv
from matplotlib import pyplot as plt
import matplotlib.ticker as ticker
import numpy as np

class AMTEA(AbstractModel):
    def __init__(self, pop_size: int, memory_size : int, lst_tasks : List[AbstractTask], model_name = "gpt", num_solvers=2, alpha = 0.2):
        self.pop_size = pop_size
        self.lst_tasks = lst_tasks
        self.memory_size = memory_size
        self.num_solvers = num_solvers
        self.population = Population(self.lst_tasks, size=pop_size, memory_size=self.memory_size)

        self.alpha_start = alpha
        self.alpha = alpha

        load_dotenv()
        print(f'Initializing LLM model: {model_name}')
        print(f'Initial alpha: {self.alpha}')
        model = init_llm_model(model_name)
        self.llm = LLM(model)
        
        num_llm_solvers = 0
        lst_solvers = []
        ga_solver = Solver('ga', 'Simulated Binary Crossover (SBX) combined with Polynomial Mutation: This operator generates an offspring population by pairing parents from the given population, performing SBX crossover on each pair, and then applying polynomial mutation to introduce additional diversity.', alpha = self.alpha)
        de_solver = Solver('de', 'Differential Evolution (DE) Crossover: This operator generates an offspring population by applying DE/rand/1 mutation and binomial crossover to each individual in the given population.', alpha=self.alpha)    
        
        print(f'Initializing {num_llm_solvers} LLM-based solvers to choose top {num_solvers} solvers.')
        while len(lst_solvers) < num_llm_solvers + 2:
            try:
                if len(lst_solvers) == 0:
                    solver = ga_solver
                elif len(lst_solvers) == 1:
                    solver = de_solver
                else:
                    [id, alg] = self.llm.init_solver()
                    solver = Solver(id, alg)
                    
                eval_scores = []
                for task_name in self.population.lst_task_names:
                    lst_indis = self.population.dict_taskpopulations[task_name].lst_indis
                    eval_scores.append(solver.evaluate_task(lst_indis, self.alpha))   
                eval_scores = np.array(eval_scores, dtype=float)
                solver.eval_score = eval_scores.mean()
                print(f'Solver {solver.id}, eval_score: {solver.eval_score}')
                lst_solvers.append(solver)
            except Exception as e:
                print('[ERROR] Create new solver failed!')
                print(e)
        lst_solvers = sorted(lst_solvers, key=lambda s: s.eval_score, reverse=True)[:num_solvers]

        lst_solver_ids = [solver.id for solver in lst_solvers]
                 
        for task_name in self.population.lst_task_names:
            self.population.dict_taskpopulations[task_name].num_solvers = len(lst_solvers)
            self.population.dict_taskpopulations[task_name].lst_solvers = lst_solvers
            self.population.dict_taskpopulations[task_name].mem.restart(lst_solver_ids)

    def run(self, eval_budget=100, lp=5, tgap=2, k=5, up=10, monitor=True, monitor_rate=1, delete_after_run=True):
        """
        Parameters
        ----------
        eval_budget : Evaluation budget
        lp : Learning period
        tgap : Transfer gap
        k : Number of individuals from each task's population to be added to the transfer pool
        up: Update period
        """
        self.dct_fitness : Dict[str, List[float]] = {}
        self.dct_diversity : Dict[str, List[float]] = {}
        for task_name in self.population.lst_task_names:
            self.dct_diversity[task_name] = []
            self.dct_fitness[task_name] = []

        self.eval_budget = eval_budget
        gen = 0
        while self.check_terminate_condition() == False:
            u = self.get_evaluation_count() / eval_budget
            self.alpha = self.alpha_start + (1.0 - self.alpha_start) * (1.0 - math.cos(math.pi * u)) / 2
            print(f'Alpha: {self.alpha}')

            for task_name in self.population.lst_task_names:
                pop = [indi.gene for indi in self.population.dict_taskpopulations[task_name].lst_indis]
                pop_mat = np.vstack([np.asarray(x, dtype=float) for x in pop])               
                self.dct_diversity[task_name].append(get_diversity(pop_mat))
                self.dct_fitness[task_name].append(self.population.dict_taskpopulations[task_name].get_best_fitness())

                if len(self.dct_fitness[task_name]) > 2:
                    if self.dct_fitness[task_name][-1] > self.dct_fitness[task_name][-2]:
                        raise ValueError("Fitness raise back!")

            gen += 1

            self.population.evolve(gen=gen, lp=lp, tgap=tgap, k=k)
            
            if monitor == True and gen % monitor_rate == 0:
                print(f'Generation {gen}:')
                print(self.population.dict_best_fitness)

            # Update solvers
            if gen % up == 0:
                self.update_solvers()
                gen = 0

        if delete_after_run: # Delete all solvers in cached folder after run
            delete_all()

    def render_history(self):
        fig, ax = plt.subplots(len(self.lst_tasks), 2)
        for i, task_name in enumerate(self.population.lst_task_names):
            ax[i, 0].plot(np.arange(len(self.dct_diversity[task_name])), np.log(self.dct_diversity[task_name]))
            ax[i, 1].plot(np.arange(len(self.dct_fitness[task_name])), self.dct_fitness[task_name])
        fig.tight_layout()

    def update_solvers(self):
        for task_name in self.population.lst_task_names:
            print(f'Updating solvers for task {task_name} ... ')
            lst_solvers = self.population.dict_taskpopulations[task_name].lst_solvers
            mem = self.population.dict_taskpopulations[task_name].mem
            best_solver_id = mem.get_best_solver_id()
            worst_solver_id = mem.get_worst_solver_id()
            good_solvers_history = self.population.dict_taskpopulations[task_name].good_solvers_history
            worst_solvers_history = self.population.dict_taskpopulations[task_name].worst_solvers_history
            
            good_solver = next((solver for solver in lst_solvers if solver.id == best_solver_id), None)
            if (good_solver.id not in [s.id for s in good_solvers_history]):
                good_solvers_history.append(good_solver)
            
            worst_solver = next((solver for solver in lst_solvers if solver.id == worst_solver_id), None)
            if (worst_solver.id not in [s.id for s in worst_solvers_history]):
                worst_solvers_history.append(worst_solver)
            
            # lst_solvers = [solver for solver in lst_solvers if solver.id != worst_solver_id]
            
            # Create new solver
            lst_indis = self.population.dict_taskpopulations[task_name].lst_indis
            eval_check_score = worst_solver.evaluate_task(lst_indis, self.alpha)
            print(f'[*] Evaluation score threshold for new solver: {eval_check_score * 0.7:.5f}')
            eval_check_count = 0
            
            for solver in lst_solvers:
                solver.eval_score = solver.evaluate_task(lst_indis, self.alpha)
                if solver.eval_score >= (eval_check_score * 0.7):
                    eval_check_count += 1
                print(f'EVAL CHECK COUNT 1: {eval_check_count}')
                print(f'Solver {solver.id}, eval_score: {solver.eval_score:.5f}')
                
            num_llm_solvers = 5
            num_try = 0
            while not (eval_check_count >= self.num_solvers and (len(lst_solvers) >= num_llm_solvers + self.num_solvers - 1)):
                num_try += 1
                if num_try > 10:
                    break

                try:
                    [id, alg] = self.llm.update_solver(good_solvers_history, worst_solvers_history, self.alpha)
                    solver = Solver(id, alg)
                    solver.eval_score = solver.evaluate_task(lst_indis, self.alpha) 
                    print(f'LLM Solver {len(lst_solvers) - self.num_solvers + 2}: {solver.id}, eval_score: {solver.eval_score:.5f}')
                    lst_solvers.append(solver)
                    if solver.eval_score >= (eval_check_score * 0.7):
                        eval_check_count += 1
                    print(f'EVAL CHECK COUNT 2: {eval_check_count}')
                except Exception as e:
                    print('[ERROR] Create new solver failed!')
                    print(e)

            lst_solvers = sorted(lst_solvers, key=lambda s: s.eval_score, reverse=True)[:self.num_solvers]
            self.population.dict_taskpopulations[task_name].lst_solvers = lst_solvers
            mem.restart([solver.id for solver in lst_solvers])
    
    def check_terminate_condition(self) -> bool:
        eval_cnt = 0
        for task in self.lst_tasks:
            eval_cnt += task.eval_cnt
        print(f'Evaluation count: {eval_cnt}/{self.eval_budget}')
        return eval_cnt >= self.eval_budget

    def get_evaluation_count(self) -> int:
        eval_cnt = 0
        for task in self.lst_tasks:
            eval_cnt += task.eval_cnt
        return eval_cnt