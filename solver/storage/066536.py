import numpy as np

def crossover(parent1, parent2):
    dim = len(parent1)
    offspring = np.zeros(dim)
    
    for i in range(dim):
        mean_value = (parent1[i] + parent2[i]) / 2
        variance = abs(parent1[i] - parent2[i])
        
        # Define adaptive scaling based on variance
        scaling_factor = 0.5 if variance > 0 else 0.1
        lower = max(0.0, mean_value - scaling_factor * variance)
        upper = min(1.0, mean_value + scaling_factor * variance)
        
        # Randomly sample within the adaptive range
        random_value = np.random.uniform(lower, upper)
        alpha = np.random.rand()
        offspring[i] = alpha * random_value + (1 - alpha) * mean_value
        
        # Ensure the offspring stays within bounds
        offspring[i] = np.clip(offspring[i], 0.0, 1.0)

    return offspring