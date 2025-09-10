import numpy as np

def crossover(parent1, parent2):
    dim = len(parent1)
    offspring = np.zeros(dim)
    alpha = np.random.rand(dim)  # Random weights for blending
    
    for i in range(dim):
        # Calculate gene distances and determine blending factor
        distance = abs(parent1[i] - parent2[i])
        if distance < 1e-6:  # Prevent division by zero
            blend_factor = 0.5
        else:
            blend_factor = distance / (distance + 1)  # Normalized distance

        cmin = min(parent1[i], parent2[i])
        cmax = max(parent1[i], parent2[i])
        I = cmax - cmin
        lower = cmin - 0.5 * I
        upper = cmax + 0.5 * I
        
        # Blend values using the determined blend factor
        blend_value = np.random.uniform(lower, upper)
        offspring[i] = blend_factor * blended_value + (1 - blend_factor) * parent1[i]
        offspring[i] = np.clip(offspring[i], 0.0, 1.0)
        
    return offspring