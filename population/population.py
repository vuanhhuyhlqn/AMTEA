from typing import List
from task import AbstractTask
from indi import Individual
from subpopulation import SubPopulation
import numpy as np

class Population:
    def __init__(self, lst_tasks: List[AbstractTask], size):
        self.lst_tasks: List[AbstractTask] = lst_tasks
        self.lst_subpopulations: List[SubPopulation] = []
        self.size = size

        for i in range(len(self.lst_tasks)):
            self.lst_subpopulations.append(SubPopulation(self.lst_tasks[i]))

        
    def load_pop(self, path:str):
        pass

    def save_pop(self, path:str):
        pass

