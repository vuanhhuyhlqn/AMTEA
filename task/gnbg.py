import numpy as np
from .abstract import AbstractTask
from .GNBG import GNBG_instances

class GNBGTask(AbstractTask):
    def __init__(self, id : int, bound: float):
        super().__init__(f'GNBG_{id}', -bound, bound, 30)
        self.gnbg = GNBG_instances.get_gnbg(id)
        self.bound = bound

    def eval(self, gene):
        decoded_gene = self.decode(gene=gene)
        return self.gnbg.fitness(decoded_gene)[0]