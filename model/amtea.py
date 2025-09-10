from typing import List, Dict
from .abstract import AbstractModel
from population import Population
from memory import Memory
from task import AbstractTask
from solver import Solver
import inspect
from utils.llm_client.openai import OpenAIClient
from utils.utils import *
from LLM.llm import LLM
import os
from dotenv import load_dotenv

load_dotenv()
GPT_API_KEY = os.getenv("GPT_API_KEY")

class AMTEA(AbstractModel):
    def __init__(self, pop_size: int, memory_size : int, lst_tasks : List[AbstractTask], num_solvers: int):
        self.pop_size = pop_size
        self.lst_tasks = lst_tasks
        self.memory_size = memory_size

        lst_task_names = [task.task_name for task in self.lst_tasks]
        self.mem = Memory(lst_task_names=lst_task_names, memory_size=memory_size)
        self.population = Population(self.lst_tasks, size=pop_size, mem=self.mem)
        
        # For evaluating solvers
        parent_pairs = self.get_parent_pairs()
        
        # LLM to init solvers
        client = OpenAIClient(model='gpt-4o-mini',temperature=1.0, api_key=GPT_API_KEY)
        self.llm = LLM("chat.openai.com", GPT_API_KEY, client)
        
        # Số lượng solvers khởi tạo để chọn lọc solvers tốt
        num_llm_solvers = 10
        lst_solvers = []
        for i in range(num_llm_solvers):
            [id, alg] = self.llm.init()
            solver = Solver(id, alg)
            solver.evaluate(parent_pairs)
            print(f'Solver {solver.id}, eval score: {solver.eval_score}')
            lst_solvers.append(solver)
        lst_solvers = sorted(lst_solvers, key=lambda s: s.eval_score, reverse=True)
        good_solvers = lst_solvers[:num_solvers]
        bad_solvers = lst_solvers[num_solvers:]
        for solver in bad_solvers:
            delete_solver_file(solver.id)  
        self.lst_solvers = good_solvers
        
        self.population.num_solvers = num_solvers
        self.population.lst_solvers = self.lst_solvers
        
        for task_name in self.population.lst_task_names:
            self.population.dict_taskpopulations[task_name].num_solvers = num_solvers
            self.population.dict_taskpopulations[task_name].lst_solvers = self.lst_solvers
            
        lst_solver_ids = [solver.id for solver in self.lst_solvers]
        self.mem.lst_solver_ids = lst_solver_ids
        self.mem.restart(self.mem.lst_solver_ids)

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
            if gen % lp <= lp - self.memory_size and gen % tgap == 0:
                print(f'[*] Knowledge transfer')
                self.population.knowledge_transfer(k=k)

            self.population.evolve(gen)
            
            if monitor == True and gen % monitor_rate == 0:
                print(f'Generation {gen}:')
                print(self.population.dict_best_fitness)

            # Update solvers
            if gen % up == 0:
                self.update_solvers()
                gen = 0
                    
    def update_solvers(self, new_solver = Solver(id='659723', algorithm='')):
        dict_avg_p_values : Dict[str, float] = {}
        for solver in self.lst_solvers:
            dict_avg_p_values[solver.id] = self.mem.get_avg_p_value(solver_id=solver.id)
        
        worst_solver_id = min(dict_avg_p_values, key=dict_avg_p_values.get)
        print(f'Worst_solver_id: {worst_solver_id}')

        self.lst_solvers = [solver for solver in self.lst_solvers if solver.id != worst_solver_id]
        self.lst_solvers.append(new_solver)
        self.population.update_solvers(self.lst_solvers)
    
    def check_terminate_condition(self) -> bool:
        eval_cnt = 0
        for task in self.lst_tasks:
            eval_cnt += task.eval_cnt
        print(f'Evaluation count: {eval_cnt}/{self.eval_budget}')
        return eval_cnt >= self.eval_budget
    
    def get_parent_pairs(self) -> List:
        parent_pairs = []
        for task_name in self.population.lst_task_names:
            lst_indis = self.population.dict_taskpopulations[task_name].lst_indis
            for i in range(0, len(lst_indis) - 1, 2):
                p1 = lst_indis[i]
                p2 = lst_indis[i + 1]
                parent_pairs.append((p1, p2))
        return parent_pairs
