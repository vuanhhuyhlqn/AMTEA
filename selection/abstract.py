from typing import List
from indi import Individual

class AbstractSelection:
    def __init__(self):
        pass

    def __call__(self, lst_indis : List[Individual]) -> List[Individual]:
        pass