from .abstract import AbstractSelection
from typing import List
from indi import Individual
import numpy as np

class TournamentSelection(AbstractSelection):
    def __init__(self, size, k):
        self.size = size
        self.k = k
    
    def __call__(self, lst_indis: List[Individual]) -> Individual:
        ret : List[Individual] = []
        
        while len(ret) < self.size:
            pool : List[Individual] = []
            while len(pool) < self.k:
                rnd_id = np.random.randint(low=0, high=len(lst_indis))
                pool.append(lst_indis[rnd_id])
            
            pool = sorted(pool, key=lambda x : x.fitness)
            ret.append(pool[0]) 
        return ret