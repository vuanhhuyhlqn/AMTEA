import numpy as np

class Individual:
	def __init__(self, dim, gene:np.ndarray=None, fitness=None):
		self.dim = dim
		if gene is None:
			self.gene = np.random.uniform(size=(self.dim))
		else:
			self.gene = gene

		if fitness is None:
			self.fitness = np.inf
		else:
			self.fitness = fitness
	def __str__(self):
		return f'{self.gene}\nFitness: {self.fitness}'