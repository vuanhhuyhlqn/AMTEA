import numpy as np
def crossover(parent1, parent2):
    dim = len(parent1)
    alpha = np.random.rand()
    mask = np.random.rand(dim) < 0.5
    offspring = np.where(mask, alpha * parent1 + (1 - alpha) * parent2, np.where(np.random.rand(dim) < 0.5, parent1, parent2))
    offspring = np.clip(offspring, 0.0, 1.0)
    return offspring