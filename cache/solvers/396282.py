import numpy as np

def crossover(parent1, parent2, grid_size=5):
    dim = len(parent1)
    grid_indices = np.floor(np.linspace(0, dim, grid_size + 1)).astype(int)
    offspring = np.zeros(dim)
    
    for i in range(dim):
        grid_position = np.digitize(i, grid_indices) - 1
        if (grid_position % 2) == 0:
            offspring[i] = parent1[i]
        else:
            offspring[i] = parent2[i]
    
    offspring = np.clip(offspring, 0.0, 1.0)
    return offspring