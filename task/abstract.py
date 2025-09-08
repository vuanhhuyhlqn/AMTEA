class AbstractTask:
    def __init__(self, task_name, dim):
        self.task_name = task_name
        self.dim = dim

    def eval(self, genes):
        pass

    def __str__(self):
        return f'Task name: {self.task_name}, dimension: {self.dim}'