from task import AbstractTask

class TaskPopulation:
    def __init__(self, task:AbstractTask, size):
        self.task = task
        self.size = size