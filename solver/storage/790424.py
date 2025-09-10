import numpy as np
def crossover(parent1, parent2):
    dim = len(parent1)
    offspring = np.copy(parent1)
    start_index = np.random.randint(dim)
    for i in range(start_index, start_index + dim):
        if i % dim < dim // 2:
            offspring[i % dim] = parent2[i % dim]
    offspring = np.clip(offspring, 0.0, 1.0)
    return offspring