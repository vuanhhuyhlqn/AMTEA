from .abstract import AbstractSelection
from typing import List
from indi import Individual
import numpy as np

class TournamentSelection(AbstractSelection):
    def __init__(self, size, k = 2):
        self.size = size
        self.k = k
    
    def __call__(self, lst_indis: List[Individual]) -> List[Individual]:
        lst_indis = sorted(lst_indis, key=lambda indi : indi.fitness)

        ret = []
        ret.append(lst_indis[0])
        
        while len(ret) < self.size:
            idxs = np.random.choice(len(lst_indis), self.k, replace=False)
            pool = [lst_indis[i] for i in idxs]
            best = min(pool, key=lambda x: x.fitness)  
            ret.append(best)
        return ret