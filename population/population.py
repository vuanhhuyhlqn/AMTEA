from typing import List
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
                 num_solvers,
                 initial_lst_solvers: List[Solver],
                 mem: Memory):
        self.lst_tasks: List[AbstractTask] = lst_tasks
        self.lst_taskpopulations: List[TaskPopulation] = []
        self.size = size
        self.num_solvers = num_solvers
        self.lst_solvers = initial_lst_solvers
        self.mem = mem

        for i in range(len(self.lst_tasks)):
            self.lst_taskpopulations.append(TaskPopulation(task=self.lst_tasks[i], 
                                                           lst_solvers=self.lst_solvers,
                                                           size=int(self / len(self.lst_tasks)),
                                                           mem=self.mem))
        
    def load_pop(self, path:str):
        # TODO implement this if have time
        pass

    def save_pop(self, path:str):
        # TODO implement this if have time
        pass

    
