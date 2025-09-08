from task import AbstractTask
from subpopulation import SubPopulation

class TaskPopulation:
    def __init__(self, task:AbstractTask, size):
        self.task = task
        self.size = size

        