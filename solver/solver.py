import sys
from os import path
from typing import List
import numpy as np
import subprocess
import time
import math

class Solver:
	def __init__(self, id: str, algorithm: str, alpha: float = 0.4, eval_score=None):
		self.id = id
		self.algorithm = algorithm
		self.alpha = alpha
		if eval_score is None:
			self.eval_score = 0.0
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
	
	def evaluate_task(self, population, alpha : float):
		all_genes = np.vstack([np.asarray(ind.gene) for ind in population])
		all_fitness = np.array([ind.fitness for ind in population])

		assert(len(population) >= 5)
		top_idx = np.argsort(all_fitness)[5:]
		top_genes = all_genes[top_idx]
		
		parent_genes = [np.asarray(ind.gene) for ind in population]
		num_test = 3
		score = 0

		for _ in range(num_test):
			offspring_genes = self(parent_genes)

			assert(len(offspring_genes.shape) == 2)
			n, d = offspring_genes.shape

			distance_to_top_genes = offspring_genes[:, None, :] - top_genes[None, :, :]
			distance_to_top_genes = np.linalg.norm(distance_to_top_genes, axis=2)
			nearist_distance_to_top_genes = np.min(distance_to_top_genes, axis=1)

			exploit_score = 1.0 - np.sum(nearist_distance_to_top_genes) / offspring_genes.shape[0] / math.sqrt(d)
			
			all_distances = offspring_genes[:, None, :] - offspring_genes[None, :, :]
			all_distances = np.linalg.norm(all_distances, axis=2)
			assert(all_distances.shape[0] == all_distances.shape[1]) # The distance matrix must be a square
			total_distance = np.triu(all_distances, k=1).sum()

			explore_score = total_distance / (n * (n - 1) / 2) / math.sqrt(d)
			
			assert(alpha >= 0.0 and alpha <= 1.0)
			print(f'Solver\'s id: {self.id}, exploit score: {exploit_score}, explore score: {explore_score}')
			score += exploit_score * alpha + explore_score * (1.0 - alpha) # TODO: Check these values

		score /= num_test # Get average score

		return score
			
		
		