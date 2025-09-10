import numpy as np

def crossover(parent1, parent2):
    dim = len(parent1)
    offspring = np.zeros(dim)
    
    for i in range(dim):
        # Calculate weighted mean and gradient between parents
        mean_value = (parent1[i] + parent2[i]) / 2
        gradient = parent1[i] - parent2[i]
        
        # Define a dynamically adjusted range based on the gradient
        lower = max(0.0, mean_value - 0.5 * abs(gradient))
        upper = min(1.0, mean_value + 0.5 * abs(gradient))
        
        # Randomly sample within the adjusted range
        random_value = np.random.uniform(lower, upper)
        alpha = np.random.rand()
        offspring[i] = alpha * random_value + (1 - alpha) * mean_value
        
        # Ensure the offspring stays within bounds
        offspring[i] = np.clip(offspring[i], 0.0, 1.0)

    return offspring