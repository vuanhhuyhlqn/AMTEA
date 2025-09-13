import sys
from os import path
from typing import List
import numpy as np
import subprocess
import time

class Solver:
	def __init__(self, id: str, algorithm: str, eval_score=None):
		self.id = id
		self.algorithm = algorithm
		if eval_score is None:
			self.eval_score = -np.inf
		else:
			self.eval_score = eval_score

	def __call__(self, operands: np.ndarray) -> np.ndarray:
		# start = time.time()
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
			# end = time.time()
			# print(f'Solver {self.id} executed successfully, time taken: {end - start}')
			assert(len(result_array) == len(operands))
			return result_array
		except Exception as e:
			print(f'Error loading result from output.npy: {e}')
			return None
	
	def evaluate_task(self, population, mode = "balanced"):
		all_genes = np.vstack([np.asarray(ind.gene) for ind in population])
		all_fitness = np.array([ind.fitness for ind in population])

		best_idx = np.argmin(all_fitness)
		worst_idx = np.argmax(all_fitness)
		pbest_global = all_genes[best_idx]
		pworst_global = all_genes[worst_idx]

		parent_genes = [np.asarray(ind.gene) for ind in population]
		offspring_genes = self(parent_genes)  

		center = np.mean(all_genes, axis=0)
		dist_pb_pw = np.linalg.norm(pworst_global - pbest_global) + 1e-12
		max_dist = max(np.linalg.norm(g - center) for g in all_genes) + 1e-12

		scores = []
		for off in offspring_genes:
			if not np.all((off >= 0.0) & (off <= 1.0)):
				return 0.0

			dist_off_pb = np.linalg.norm(off - pbest_global)

			RPB = max(0.0, (dist_pb_pw - dist_off_pb) / dist_pb_pw)

			dist_mean = np.linalg.norm(off - center) + 1e-12
			DS = dist_mean / max_dist
			
			if mode == "exploit":
				score = 0.6 * RPB + 0.4 * (1.0 - DS)
			elif mode == "explore":
				score = 0.3 * RPB + 0.7 * DS
			else:
				score = 0.5 * RPB + 0.5 * DS
    
			scores.append(score)

		scores = np.array(scores, dtype=float)
		task_score = float(scores.mean())
		return task_score
			
		
		