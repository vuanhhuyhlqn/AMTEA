from getParas import Paras
from utils.utils import *
from LLM.llm import LLM
from solver.solver import Solver
import numpy as np

class TestLLM:
    def __init__(self, cfg, client) -> None:
        self.cfg = cfg
        
        self.paras = Paras()
        self.paras.set_paras(llm_model = client)
        
        init_client(cfg)
        
        self.llm = LLM(self.paras.llm_api_endpoint, self.cfg.llm_client.api_key, client)
        
    def run(self):
        
        [code, alg] = self.llm.init()
        
        solver = Solver(save_code_to_solver_folder(code))
        
        parent1 = np.array([0.1, 0.2, 0.3, 0.4, 0.5])
        parent2 = np.array([0.9, 0.8, 0.7, 0.6, 0.5])

        print("Cha:", parent1)
        print("Mẹ:", parent2)
        
        offspring = solver([parent1, parent2])
        print("Con:", offspring)
        
        return [code, alg]