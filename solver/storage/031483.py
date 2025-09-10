import numpy as np

def crossover(parent1, parent2, mu=0.1):
    dim = len(parent1)
    offspring = np.zeros(dim)
    for i in range(dim):
        diff = parent2[i] - parent1[i]
        mutation = mu * diff
        offspring[i] = parent1[i] + mutation
        offspring[i] = np.clip(offspring[i], 0.0, 1.0)
    return offspring