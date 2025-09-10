import numpy as np

def crossover(parent1, parent2):
    dim = len(parent1)
    offspring = np.zeros(dim)
    
    for i in range(dim):
        diff = abs(parent1[i] - parent2[i])
        alpha = np.random.rand() if diff > 0 else 0.5  # Avoid division by zero
        
        # Blend Interval
        cmin = min(parent1[i], parent2[i])
        cmax = max(parent1[i], parent2[i])
        lower = cmin - alpha * diff
        upper = cmax + alpha * diff

        # Generate Offspring
        offspring[i] = np.random.uniform(lower, upper)
        offspring[i] = np.clip(offspring[i], 0.0, 1.0)

    return offspring