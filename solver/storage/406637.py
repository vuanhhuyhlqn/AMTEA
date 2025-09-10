import numpy as np

def crossover(parent1, parent2):
    dim = len(parent1)
    offspring = np.zeros(dim)
    
    for i in range(dim):
        mean_value = (parent1[i] + parent2[i]) / 2
        distance = abs(parent1[i] - parent2[i])
        
        # Dynamically adjust the blending factor based on distance
        if distance > 0:
            alpha = max(0.5, np.random.rand() * (1 - (distance / 2)))  # Ensure more weight given to the mean
        else:
            alpha = 1.0  # If both parents are the same, use full mean
        
        # Sample within an adjusted range around the mean
        lower = max(0.0, mean_value - distance * 0.5)
        upper = min(1.0, mean_value + distance * 0.5)
        
        random_value = np.random.uniform(lower, upper)
        offspring[i] = alpha * random_value + (1 - alpha) * mean_value
        
        # Ensure the offspring stays within bounds
        offspring[i] = np.clip(offspring[i], 0.0, 1.0)

    return offspring