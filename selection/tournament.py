from .abstract import AbstractSelection
from typing import List
from indi import Individual
import numpy as np

class TournamentSelection(AbstractSelection):
    def __init__(self, size, k):
        self.size = size
        self.k = k
    
    def __call__(self, lst_indis: List[Individual]) -> List[Individual]:
        ret = []
        for _ in range(self.size):
            idxs = np.random.choice(len(lst_indis), self.k, replace=False)
            pool = [lst_indis[i] for i in idxs]
            best = min(pool, key=lambda x: x.fitness)  
            ret.append(best)
        return ret