import sys
from os import path
from typing import List
import numpy as np
import subprocess
import time

# TODO: implement batch crossover
class Solver:
    def __init__(self, id: str, algorithm: str):
        self.id = id
        self.algorithm = algorithm
        self.eval_score = -np.inf

    def __call__(self, operands: List[np.ndarray]) -> np.ndarray:
        start = time.time()
        if len(operands) != self.num_operands:
            print('Number of operands doesn\'t match')
            return None

        # print(f'Running solver {self.id}')
        temp_dir = path.join(path.dirname(__file__), 'temp')
        temp_file = path.join(temp_dir, 'temp_parents.npy')
        np.save(temp_file, operands, allow_pickle=True)
        
        run_file = path.join(path.dirname(__file__), 'run.py')
        run_file = path.abspath(run_file)
        output_file = path.join(temp_dir, 'output.npy')
        
        try:
            subprocess.run(
                [sys.executable, run_file, self.id],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=True
            )
        except subprocess.CalledProcessError as e:
            print(f'Error running run.py: {e.stderr.decode()}')
            return None

        try:
            result_array = np.load(output_file, allow_pickle=True)
            end = time.time()
            print(f'Sovler {self.id} executed successfully, time taken: {end - start}')
            return result_array
        except Exception as e:
            print(f'Error loading result from output.npy: {e}')
            return None
    
    def evaluate(self, parent_pairs):
        scores = []
        for (indi1, indi2) in parent_pairs:
            if indi1.fitness <= indi2.fitness:
                pbest, pworst = indi1.gene, indi2.gene
            else:
                pbest, pworst = indi2.gene, indi1.gene

            offspring = self([indi1.gene, indi2.gene])
            if offspring is None:
                score = 0.0
            else:   
                FR = 1.0 if np.all((offspring >= 0) & (offspring <= 1)) else 0.0
                
                dist_pb_pw = np.linalg.norm(pworst - pbest) + 1e-12
                RPB = 1 - np.linalg.norm(offspring - pbest) / dist_pb_pw   
                
                dist_par = np.linalg.norm(indi1.gene - indi2.gene) + 1e-12
                DS = ((np.linalg.norm(offspring - indi1.gene) + np.linalg.norm(offspring - indi2.gene))
                / (2 * dist_par))

                score = 0.4 * FR + 0.4 * RPB + 0.2 * DS
            scores.append(score)
        
        scores = np.array(scores)
        self.eval_score = scores.mean()
            
        
        