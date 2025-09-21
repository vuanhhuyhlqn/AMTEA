from typing import List, Dict, Tuple
from collections import deque
import numpy as np
import pandas as pd

class Memory():
	def __init__(self, memory_size: int = 30):
		self.memory_size = memory_size
  
		self.succ: deque[Tuple[int, int]] = deque()
		self.fail: deque[Tuple[int, int]] = deque()
  
		self.succ_p = [0.5, 0.5]
  
		self.lst_solver_ids = []
		self.p_values: Dict[str, float] = {}

	def restart(self, lst_solver_ids: List[str]):
		self.succ.clear()
		self.fail.clear()
		self.p_data: Dict[str, float] = {}

		self.lst_solver_ids = lst_solver_ids
		self.succ_p = [0.5, 0.5]

		self.update_p_values_to_dict()
   
	def add_succ(self, tuple: Tuple[int, int]):
		self.succ.append(tuple)
		if len(self.succ) > self.memory_size:
			self.succ.popleft()

	def add_fail(self, tuple: Tuple[int, int]):
		self.fail.append(tuple)
		if len(self.fail) > self.memory_size:
			self.fail.popleft()
   
	def cal_succ_p(self):
		# print(f'Current success probabilities: {self.succ_p}')
		succ_p = []
		sums_succ = [sum(solver) for solver in zip(*self.succ)]
		sums_fail = [sum(solver) for solver in zip(*self.fail)]

		for i in range(len(self.lst_solver_ids)):
			if (sums_succ[i] + sums_fail[i]) == 0:
				succ_p.append(0.01)
			else:
				succ_p.append(sums_succ[i] / (sums_succ[i] + sums_fail[i]))
		
		succ_p = np.array(succ_p)
		self.succ_p = np.array(self.succ_p)	
		succ_p = self.succ_p / 2 + succ_p
		succ_p = succ_p / sum(succ_p)
		self.succ_p = succ_p
		self.succ_p = self.succ_p.tolist()
		# print(f'Updated success probabilities: {self.succ_p}')
  
		self.update_p_values_to_dict()
  
	def update_p_values_to_dict(self):
			for i, solver_id in enumerate(self.lst_solver_ids):
				self.p_values[solver_id] = self.succ_p[i]
    
	def get_best_solver_id(self):
		best_solver_id = self.lst_solver_ids[0]

		if self.succ_p[0] < self.succ_p[1]:
			best_solver_id = self.lst_solver_ids[1]
		return best_solver_id

	def get_worst_solver_id(self):
		worst_solver_id = self.lst_solver_ids[0]

		if self.succ_p[0] > self.succ_p[1]:
			worst_solver_id = self.lst_solver_ids[1]
		return worst_solver_id
