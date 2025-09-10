import numpy as np
def crossover(parent1, parent2):
    dim = len(parent1)
    offspring = np.zeros(dim)
    for i in range(dim):
        if abs(parent1[i] - 0.5) < abs(parent2[i] - 0.5):
            offspring[i] = parent1[i]
        else:
            offspring[i] = parent2[i]
        offspring[i] = np.clip(offspring[i], 0.0, 1.0)
    return offspring