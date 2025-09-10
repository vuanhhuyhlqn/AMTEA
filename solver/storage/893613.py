import numpy as np

def crossover(parent1, parent2, alpha=0.5):
    dim = len(parent1)
    offspring = np.zeros(dim)
    for i in range(dim):
        lower_bound = min(parent1[i], parent2[i]) - alpha * abs(parent1[i] - parent2[i])
        upper_bound = max(parent1[i], parent2[i]) + alpha * abs(parent1[i] - parent2[i])
        
        offspring[i] = np.random.uniform(lower_bound, upper_bound)
        
    return offspring