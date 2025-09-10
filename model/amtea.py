from typing import List
from .abstract import AbstractModel
from population import Population
from memory import Memory
from task import AbstractTask
from solver import Solver

class AMTEA(AbstractModel):
    def __init__(self, pop_size: int, memory_size : int, lst_tasks : List[AbstractTask], initial_lst_solvers: List[Solver]):
        self.pop_size = pop_size
        self.lst_tasks = lst_tasks
        self.initial_lst_solvers = initial_lst_solvers

        lst_task_names = [task.task_name for task in self.lst_tasks]
        initial_solver_ids = [solver.id for solver in self.initial_lst_solvers]

        self.mem = Memory(lst_task_names=lst_task_names,
                          initial_solver_ids=initial_solver_ids,
                          memory_size=memory_size)
        
        self.population = Population(self.lst_tasks,
                                     size=pop_size,
                                     initial_lst_solvers=self.initial_lst_solvers,
                                     mem=self.mem)

    def run(self, num_gen=1, monitor=True, monitor_rate=1):
        for gen in range(1, num_gen + 1):
            self.population.evolve(gen)
            if monitor == True and gen % monitor_rate == 0:
                print(f'Generation {gen}:')
                print(self.population.dict_best_fitness)
                    

