import numpy as np

def crossover(parent1, parent2, poly_degree=3):
    dim = len(parent1)
    offspring = np.zeros(dim)
    
    for i in range(dim):
        u = np.random.rand()
        offspring[i] = (1 - u) * parent1[i] + u * parent2[i]
        for d in range(1, poly_degree + 1):
            offspring[i] += (np.random.rand() - 0.5) * (parent2[i] - parent1[i]) * (u ** d)
    
    offspring = np.clip(offspring, 0.0, 1.0)
    return offspring