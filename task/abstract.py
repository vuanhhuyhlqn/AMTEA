import numpy as np

class AbstractTask:
    def __init__(self, task_name : str, upper_bound: float, lower_bound : float, dim : int):
        self.task_name = task_name
        self.upper_bound = upper_bound
        self.lower_bound = lower_bound
        self.dim = dim
        self.eval_cnt = 0

    def decode(self, gene : np.ndarray):
        decoded_gene = (gene * (self.upper_bound - self.lower_bound) + self.lower_bound)[:self.dim]
        return decoded_gene
    
    def batch_decode(self, genes: np.ndarray):
        decoded_genes = (genes * (self.upper_bound - self.lower_bound) + self.lower_bound)[:, :self.dim]
        return decoded_genes

    def eval(self, gene : np.ndarray) -> float:
        pass

    def __str__(self):
        return f'Task name: {self.task_name}, dimension: {self.dim}'