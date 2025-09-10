import numpy as np
def crossover(parent1, parent2):
    dim = len(parent1)
    offspring = np.zeros(dim)
    for i in range(dim):
        distance = abs(parent1[i] - parent2[i])
        alpha = np.random.rand() * (1 + distance)  # Adjust the mixing ratio based on distance
        offspring[i] = alpha * parent1[i] + (1 - alpha) * parent2[i]
        offspring[i] = np.clip(offspring[i], 0.0, 1.0)
    return offspring