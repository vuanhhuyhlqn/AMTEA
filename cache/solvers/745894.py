import numpy as np

def crossover(parent1, parent2, sigma=0.1):
    dim = len(parent1)
    offspring = np.zeros(dim)
    
    # Calculate the mean of the two parents
    mean = (parent1 + parent2) / 2
    
    for i in range(dim):
        # Add Gaussian noise to the mean
        offspring[i] = mean[i] + np.random.normal(0, sigma)

    # Ensure the offspring stays within the bounds [0, 1]
    offspring = np.clip(offspring, 0.0, 1.0)
    return offspring