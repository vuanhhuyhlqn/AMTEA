import numpy as np

def crossover(parent1, parent2):
    dim = len(parent1)
    offspring = np.zeros(dim)
    
    for i in range(dim):
        mean_value = (parent1[i] + parent2[i]) / 2
        distance = abs(parent1[i] - parent2[i])
        
        # Define a dynamically adjusted range around the parents
        lower = max(0.0, mean_value - distance)
        upper = min(1.0, mean_value + distance)
        
        # Randomly sample within the adjusted range
        random_value = np.random.uniform(lower, upper)
        
        # Blend with a weighted mean
        alpha = np.random.rand()  # Random weight for blending with the mean
        offspring[i] = alpha * random_value + (1 - alpha) * mean_value
        
        # Ensure the offspring stays within bounds
        offspring[i] = np.clip(offspring[i], 0.0, 1.0)

    return offspring