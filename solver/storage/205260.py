import numpy as np

def crossover(parent1, parent2):
    dim = len(parent1)
    weights = np.random.rand(dim)
    total_weight = np.sum(weights)
    weights /= total_weight  # Normalize weights
    offspring = weights * parent1 + (1 - weights) * parent2
    offspring = np.clip(offspring, 0.0, 1.0)
    return offspring