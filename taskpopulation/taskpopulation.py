from typing import List
from task import AbstractTask
from subpopulation import SubPopulation
from solver import Solver

class TaskPopulation:
    def __init__(self, task:AbstractTask, size, lst_solvers: List[Solver]):
        self.task = task
        self.size = size
        self.lst_solvers = lst_solvers


        