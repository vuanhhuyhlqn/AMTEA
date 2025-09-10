import numpy as np

def crossover(parent1, parent2):
    dim = len(parent1)
    offspring = np.zeros(dim)
    variances = np.abs(parent1 - parent2)
    for i in range(dim):
        if np.random.rand() < 0.5:
            # Use a blending weight based on the variance
            alpha = np.random.rand() * variances[i]
            offspring[i] = alpha * parent1[i] + (1 - alpha) * parent2[i]
        else:
            offspring[i] = np.random.choice([parent1[i], parent2[i]])
        offspring[i] = np.clip(offspring[i], 0.0, 1.0)
    return offspring