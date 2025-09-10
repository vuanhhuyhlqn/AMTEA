import numpy as np

def crossover(parent1, parent2, alpha=0.5, mutation_rate=0.1):
    dim = len(parent1)
    offspring = np.zeros(dim)
    
    for i in range(dim):
        # Weighted average to blend traits
        offspring[i] = np.clip(alpha * parent1[i] + (1 - alpha) * parent2[i], 0.0, 1.0)
        
        # Apply differential mutation
        if np.random.rand() < mutation_rate:
            mutation = np.random.uniform(-0.1, 0.1)
            offspring[i] = np.clip(offspring[i] + mutation, 0.0, 1.0)
    
    return offspring