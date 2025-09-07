from typing import List
from task import AbstractTask
from indi import Individual
from subpopulation import SubPopulation

class Population:
    def __init__(self, lst_tasks: List[AbstractTask], size, load_path=None):
        self.lst_tasks: List[AbstractTask] = lst_tasks
        self.lst_indis: List[Individual] = []
        self.size = size


        if load_path is not None:
            pass
        else:
            pass
        
    def load_pop(self, path:str):
        pass

    def save_pop(self, path:str):
        pass

