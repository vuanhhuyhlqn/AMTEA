import numpy as np

def crossover(parent1, parent2, F=0.5, alpha=0.3):
    dim = len(parent1)
    offspring = np.zeros(dim)
    for i in range(dim):
        cmin = min(parent1[i], parent2[i])
        cmax = max(parent1[i], parent2[i])
        I = cmax - cmin
        lower = cmin - alpha * I
        upper = cmax + alpha * I
        
        # Dynamic weighting based on parent distance
        weight = np.random.rand() * (1 - np.abs(parent1[i] - parent2[i]))
        if np.random.rand() < 0.5:
            offspring[i] = np.random.uniform(lower, upper)
        else:
            j_rand = np.random.randint(dim)
            if np.random.rand() < 0.9 or i == j_rand:
                offspring[i] = parent1[i] + weight * F * (parent2[i] - parent1[i])
            else:
                offspring[i] = parent1[i]
        
        offspring[i] = np.clip(offspring[i], 0.0, 1.0)
    return offspring