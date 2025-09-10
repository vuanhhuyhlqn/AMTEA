import numpy as np

def crossover(parent1, parent2):
    dim = len(parent1)
    offspring = np.zeros(dim)
    weights = np.random.rand(dim)  # Scaling factors for each gene
    
    for i in range(dim):
        # Calculate the range and blending bounds
        cmin = min(parent1[i], parent2[i])
        cmax = max(parent1[i], parent2[i])
        I = cmax - cmin
        lower = max(0.0, cmin - 0.5 * I)
        upper = min(1.0, cmax + 0.5 * I)
        
        # Generate a blended value within the specified range
        blend_value = np.random.uniform(lower, upper)
        offspring[i] = weights[i] * blend_value + (1 - weights[i]) * parent1[i]
        offspring[i] = np.clip(offspring[i], 0.0, 1.0)  # Ensure bounds
    
    return offspring