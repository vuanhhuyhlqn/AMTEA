from typing import List
from task import AbstractTask
from indi import Individual
from taskpopulation import TaskPopulation
from subpopulation import SubPopulation
from solver import Solver
import numpy as np

class Population:
    def __init__(self, 
                 lst_tasks: List[AbstractTask], 
                 size,
                 num_solvers,
                 lst_solvers: List[Solver]):
        self.lst_tasks: List[AbstractTask] = lst_tasks
        self.lst_taskpopulations: List[TaskPopulation] = []
        self.size = size
        self.num_solvers = num_solvers
        self.lst_solvers = lst_solvers

        for i in range(len(self.lst_tasks)):
            self.lst_taskpopulations.append(TaskPopulation(self.lst_tasks[i], int(self / len(self.lst_tasks))))
        

        
    def load_pop(self, path:str):
        pass

    def save_pop(self, path:str):
        pass

