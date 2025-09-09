import sys
from os import path
from typing import List
import numpy as np
import subprocess
# import json

class Solver:
    def __init__(self, id: str):
        self.id = id
        self.num_operands = 2  
        self.algorithm = "" # ? No need

    def __call__(self, operands: List[np.ndarray]) -> np.ndarray:
        if len(operands) != self.num_operands:
            print('Number of operands doesn\'t match')
            return None
        
        print(f'Running solver {self.id}')
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
            return result_array
        except Exception as e:
            print(f'Error loading result from output.npy: {e}')
            return None
        
        
        