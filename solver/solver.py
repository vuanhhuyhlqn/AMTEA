import sys
from os import path
from typing import List
import numpy as np

class Solver:
	def __init__(self, id):
		self.id = id
	
	def __call__(self, operands: List[np.ndarray]) -> np.ndarray:
		pass
        #TODO: run the file with solver's id
		
 