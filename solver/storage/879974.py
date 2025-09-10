import numpy as np

def crossover(parent1, parent2):
    dim = len(parent1)
    offspring = np.zeros(dim)
    
    for i in range(dim):
        mean_value = (parent1[i] + parent2[i]) / 2
        distance = abs(parent1[i] - parent2[i])
        
        # Define dynamic bounds based on the mean and distance
        lower = max(0.0, mean_value - 0.5 * distance)
        upper = min(1.0, mean_value + 0.5 * distance)

        # Generate weighted random value within the adjusted bounds
        random_value = np.random.uniform(lower, upper)
        alpha = np.random.rand()  # Randomly select blending weight
        
        # Combine mean and random value to create offspring gene
        offspring[i] = alpha * random_value + (1 - alpha) * mean_value
        offspring[i] = np.clip(offspring[i], 0.0, 1.0)

    return offspring