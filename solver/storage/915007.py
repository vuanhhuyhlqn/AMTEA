import numpy as np

def crossover(parent1, parent2):
    dim = len(parent1)
    offspring = np.zeros(dim)
    alpha = np.random.rand(dim)  # Random weights for blending
    for i in range(dim):
        cmin = min(parent1[i], parent2[i])
        cmax = max(parent1[i], parent2[i])
        I = cmax - cmin
        lower = cmin - 0.5 * I
        upper = cmax + 0.5 * I
        blend_value = np.random.uniform(lower, upper)
        offspring[i] = alpha[i] * blend_value + (1 - alpha[i]) * parent1[i]
        offspring[i] = np.clip(offspring[i], 0.0, 1.0)
    return offspring