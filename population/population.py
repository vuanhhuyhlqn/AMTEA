from typing import List, Dict
from task import AbstractTask
from indi import Individual
from taskpopulation import TaskPopulation
from subpopulation import SubPopulation
from solver import Solver
from memory import Memory
import numpy as np

class Population:
    def __init__(self, 
                 lst_tasks: List[AbstractTask], 
                 size,
                 initial_lst_solvers: List[Solver],
                 mem: Memory):
        self.lst_tasks: List[AbstractTask] = lst_tasks
        self.lst_task_names = [task.task_name for task in self.lst_tasks]
        self.dict_taskpopulations: Dict[str, TaskPopulation] = {}
        self.size = size
        self.num_solvers = len(initial_lst_solvers)
        self.lst_solvers = initial_lst_solvers
        self.mem = mem
        self.indi_dim = max([task.dim for task in self.lst_tasks])

        self.dict_best_fitness : Dict[str, float] = {}

        for i in range(len(self.lst_tasks)):
            task_name = self.lst_tasks[i].task_name
            self.dict_taskpopulations[task_name] = TaskPopulation(task=self.lst_tasks[i], 
                                                                 lst_solvers=self.lst_solvers,
                                                                 size=int(self.size / len(self.lst_tasks)),
                                                                 mem=self.mem,
                                                                 dim = self.indi_dim)
        
    
    def evolve(self, gen : int):
        for task_name in self.lst_task_names:
            self.dict_taskpopulations[task_name].evolve(gen=gen)
            self.dict_best_fitness[task_name] = self.dict_taskpopulations[task_name].get_best_fitness()

            if gen % self.mem.memory_size == 0:
                for solver in self.lst_solvers:
                    self.mem.update_p_value(task_name=task_name, solver_id=solver.id, generation=gen)
        
    def load_pop(self, path:str):
        # TODO implement this if have time
        pass

    def save_pop(self, path:str):
        # TODO implement this if have time
        pass

    
