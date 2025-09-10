import numpy as np

def crossover(parent1, parent2):
    dim = len(parent1)
    offspring = np.zeros(dim)
    
    for i in range(dim):
        mean_value = (parent1[i] + parent2[i]) / 2
        distance = abs(parent1[i] - parent2[i])
        
        # Adaptive range around the mean
        lower = max(0.0, mean_value - 0.5 * distance)
        upper = min(1.0, mean_value + 0.5 * distance)
        
        # Stochastic factor for blending
        blend_factor = np.random.rand() * 0.5 + 0.5  # Between 0.5 and 1.0
        random_value = np.random.uniform(lower, upper)
        
        # Weighted mean combining
        offspring[i] = blend_factor * random_value + (1 - blend_factor) * mean_value
        offspring[i] = np.clip(offspring[i], 0.0, 1.0)

    return offspring