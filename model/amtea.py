from typing import List, Dict
from .abstract import AbstractModel
from population import Population
from task import AbstractTask
from solver import Solver
from utils.utils import *
from LLM.llm import LLM
from dotenv import load_dotenv
import numpy as np

class AMTEA(AbstractModel):
    def __init__(self, pop_size: int, memory_size : int, lst_tasks : List[AbstractTask], model_name = "gpt", num_solvers=2):
        self.pop_size = pop_size
        self.lst_tasks = lst_tasks
        self.memory_size = memory_size
        self.num_solvers = num_solvers
        self.population = Population(self.lst_tasks, size=pop_size, memory_size=self.memory_size)
        
        load_dotenv()
        print(f'Initializing LLM model: {model_name}')
        model = init_llm_model(model_name)
        self.llm = LLM(model)
        
        num_llm_solvers = 5
        lst_solvers = []
        ga_solver = Solver('ga', 'Simulated Binary Crossover (SBX) combined with Polynomial Mutation: This operator generates an offspring population by pairing parents from the given population, performing SBX crossover on each pair, and then applying polynomial mutation to introduce additional diversity.')
        de_solver = Solver('de', 'Differential Evolution (DE) Crossover: This operator generates an offspring population by applying DE/rand/1 mutation and binomial crossover to each individual in the given population.')    
        
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
                    eval_scores.append(solver.evaluate_task(lst_indis))   
                eval_scores = np.array(eval_scores, dtype=float)
                solver.eval_score = eval_scores.mean()
                print(f'Solver {solver.id}, eval_score: {solver.eval_score}')
                lst_solvers.append(solver)
            except:
                print('[ERROR] Create new solver failed!')
        lst_solvers = sorted(lst_solvers, key=lambda s: s.eval_score, reverse=True)[:num_solvers]
        
        lst_solver_ids = []
        dict_solvers: Dict[str, Solver] = {}
        for solver in lst_solvers:
            lst_solver_ids.append(solver.id)
            dict_solvers[solver.id] = solver
                 
        for task_name in self.population.lst_task_names:
            self.population.dict_taskpopulations[task_name].num_solvers = len(lst_solvers)
            self.population.dict_taskpopulations[task_name].lst_solvers = lst_solvers
            self.population.dict_taskpopulations[task_name].dict_solvers = dict_solvers
            self.population.dict_taskpopulations[task_name].mem.restart(lst_solver_ids)

    def run(self, eval_budget=100, lp=5, tgap=2, k=5, up=10, monitor=True, monitor_rate=1):
        """
        Parameters
        ----------
        eval_budget : Evaluation budget
        lp : Learning period
        tgap : Transfer gap
        k : Number of individuals from each task's population to be added to the transfer pool
        up: Update period
        """
        self.eval_budget = eval_budget
        gen = 0
        while self.check_terminate_condition() == False:
            gen += 1
            # if gen % lp <= lp - self.memory_size and gen % tgap == 0:
            #     print(f'[*] Knowledge transfer')   

            self.population.evolve(gen=gen, lp=lp, tgap=tgap, k=k)
            
            if monitor == True and gen % monitor_rate == 0:
                print(f'Generation {gen}:')
                print(self.population.dict_best_fitness)

            # Update solvers
            if gen % up == 0:
                self.update_solvers()
                gen = 0
                
        # delete_all()
                    
    def update_solvers(self):
        for task_name in self.population.lst_task_names:
            print(f'Updating solvers for task {task_name} ... ')
            lst_solvers = self.population.dict_taskpopulations[task_name].lst_solvers
            mem = self.population.dict_taskpopulations[task_name].mem
            best_solver_id = mem.get_best_solver_id()
            worst_solver_id = mem.get_worst_solver_id()
            good_solvers_history = self.population.dict_taskpopulations[task_name].good_solvers_history
            worst_solvers_history = self.population.dict_taskpopulations[task_name].worst_solvers_history
            pdi, IR, DIc = self.population.dict_taskpopulations[task_name].compute_pdi()
            print(f'[*] PDI: {pdi}, IR: {IR}, DIc: {DIc}')
            if pdi < 0.4:
                mode = "explore"
            elif pdi > 0.6:
                mode = "exploit"
            else:
                mode = "balanced"
            print(f'[*] Update mode: {mode}')
            good_solver = next((solver for solver in lst_solvers if solver.id == best_solver_id), None)
            if (good_solver.id not in [s.id for s in good_solvers_history]):
                good_solvers_history.append(good_solver)
            
            
            worst_solver = next((solver for solver in lst_solvers if solver.id == worst_solver_id), None)
            if (worst_solver.id not in [s.id for s in worst_solvers_history]):
                worst_solvers_history.append(worst_solver)
            
            lst_solvers = [solver for solver in lst_solvers if solver != worst_solver]
            
            # Create new solver
            lst_indis = self.population.dict_taskpopulations[task_name].lst_indis
            best_eval_score = good_solver.evaluate_task(lst_indis, mode)
            print(f'Eval score of best solver: {best_eval_score}')
            num_llm_solvers = 5
            temp_lst_solvers = []
            eval_check = False
            while not (eval_check and len(temp_lst_solvers) >= num_llm_solvers + self.num_solvers):
                try:
                    [id, alg] = self.llm.update_solver(good_solvers_history, worst_solvers_history, mode)
                    solver = Solver(id, alg, mode)
                    solver.eval_score = solver.evaluate_task(lst_indis, mode) 
                    print(f'LLM Solver {len(temp_lst_solvers) + 1}: {solver.id}, eval_score: {solver.eval_score}')
                    temp_lst_solvers.append(solver)
                    if solver.eval_score >= best_eval_score:
                        eval_check = True
                except:
                    print('[ERROR] Create new solver failed!')
            temp_lst_solvers = sorted(temp_lst_solvers, key=lambda s: s.eval_score, reverse=True)
            new_solver = temp_lst_solvers[0]
            
            lst_solvers.append(new_solver)
            mem.restart([solver.id for solver in lst_solvers])
            print(f'New solver added: {new_solver.id}')
    
    def check_terminate_condition(self) -> bool:
        eval_cnt = 0
        for task in self.lst_tasks:
            eval_cnt += task.eval_cnt
        print(f'Evaluation count: {eval_cnt}/{self.eval_budget}')
        return eval_cnt >= self.eval_budget
