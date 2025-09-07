from typing import List
from ..task.abstract import AbstractTask

class Population:
    def __init__(self, lst_tasks: List[AbstractTask]):
        self.lst_tasks = lst_tasks
        
    def load_pop(self, path:str):
        pass

    def save_pop(self, path:str):
        pass

