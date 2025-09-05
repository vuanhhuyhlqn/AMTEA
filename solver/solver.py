import sys
from os import path
from typing import List
import numpy as np

class Solver:
	def __init__(self, num_operands, id):
		self.id = id
		self.num_operands = num_operands
	
	def __call__(self, operands: List[np.ndarray]) -> np.ndarray:
		if len(operands) != self.num_operands:
			print('Number of operands doesn\'t match')
			return None
		
		#TODO: run the file with solver's id
 