import numpy as np

def crossover(parent1, parent2, alpha=0.5, sigma=0.1):
    dim = len(parent1)
    offspring = np.zeros(dim)
    for i in range(dim):
        # Blend the trait values with a weighted average
        blended_value = alpha * parent1[i] + (1 - alpha) * parent2[i]
        # Add Gaussian noise to introduce variability
        noise = np.random.normal(0, sigma)
        offspring[i] = np.clip(blended_value + noise, 0.0, 1.0)
        
    return offspring