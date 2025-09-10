import numpy as np

def crossover(parent1, parent2):
    dim = len(parent1)
    mask = np.random.rand(dim) < 0.5
    alpha = np.random.rand(dim)
    offspring = np.where(mask, alpha * parent1 + (1 - alpha) * parent2, parent1 if np.random.rand(dim) < 0.5 else parent2)
    offspring = np.clip(offspring, 0.0, 1.0)
    return offspring