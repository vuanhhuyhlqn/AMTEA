import numpy as np

def crossover(parent1, parent2):
    dim = len(parent1)
    offspring = np.zeros(dim)
    
    for i in range(dim):
        mean_value = (parent1[i] + parent2[i]) / 2
        distance = abs(parent1[i] - parent2[i])
        
        # Dynamically adjust the blending factor based on distance
        alpha = 0.5 + 0.5 * (1 - (distance / 2))  # Ensure a balance between parents
        
        # Introduce a stochastic shift within a bounded range
        shift = np.random.uniform(-0.1 * distance, 0.1 * distance)
        adjusted_value = mean_value + shift
        
        # Ensure the offspring stays within bounds
        offspring[i] = np.clip(alpha * adjusted_value + (1 - alpha) * mean_value, 0.0, 1.0)

    return offspring