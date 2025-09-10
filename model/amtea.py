from typing import List, Dict
from .abstract import AbstractModel
from population import Population
from memory import Memory
from task import AbstractTask
from solver import Solver
import inspect

class AMTEA(AbstractModel):
    def __init__(self, pop_size: int, memory_size : int, lst_tasks : List[AbstractTask], initial_lst_solvers: List[Solver]):
        self.pop_size = pop_size
        self.lst_tasks = lst_tasks
        self.lst_solvers = initial_lst_solvers
        self.memory_size = memory_size

        lst_task_names = [task.task_name for task in self.lst_tasks]
        lst_solver_ids = [solver.id for solver in self.lst_solvers]

        self.mem = Memory(lst_task_names=lst_task_names,
                          initial_solver_ids=lst_solver_ids,
                          memory_size=memory_size)
        
        self.population = Population(self.lst_tasks,
                                     size=pop_size,
                                     lst_solvers=self.lst_solvers,
                                     mem=self.mem)

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
                    
    def update_solvers(self, new_solver = Solver(id='659723')):
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
