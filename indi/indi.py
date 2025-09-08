import numpy as np

class Individual:
    def __init__(self, dim, gene=None):
        self.dim = dim
        if gene is None:
            self.gene = np.random.uniform(size=(self.dim))
        else:
            self.gene = gene

        self.fitness = np.inf

    def __str__(self):
        return f'{self.gene}\nFitness: {self.fitness}'
    
    def __lt__(self, other):
        return self.fitness < other.fitness