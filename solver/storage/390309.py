import numpy as np

def crossover(parent1, parent2):
    dim = len(parent1)
    offspring = np.zeros(dim)
    
    for i in range(dim):
        mean_value = (parent1[i] + parent2[i]) / 2
        distance = abs(parent1[i] - parent2[i])
        
        lower = max(0.0, mean_value - distance)
        upper = min(1.0, mean_value + distance)
        
        random_value = np.random.uniform(lower, upper)
        alpha = np.random.rand() * 0.3 + 0.7  # Ensure alpha is more weighted towards the random sample
        
        offspring[i] = alpha * random_value + (1 - alpha) * mean_value
        offspring[i] = np.clip(offspring[i], 0.0, 1.0)

    return offspring