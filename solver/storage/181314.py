import numpy as np

def crossover(parent1, parent2):
    dim = len(parent1)
    offspring = np.zeros(dim)
    
    alpha = np.random.rand(dim)  # Random weights for blending
    for i in range(dim):
        # Blending between parents
        blend_value = alpha[i] * parent1[i] + (1 - alpha[i]) * parent2[i]
        
        # Stochastic decision for exploration
        explore = np.random.rand()
        if explore < 0.5:
            # Sample within an extended range
            cmin = min(parent1[i], parent2[i])
            cmax = max(parent1[i], parent2[i])
            I = cmax - cmin
            lower = np.clip(cmin - 0.5 * I, 0.0, 1.0)
            upper = np.clip(cmax + 0.5 * I, 0.0, 1.0)
            offspring[i] = np.random.uniform(lower, upper)
        else:
            offspring[i] = blend_value
        
        # Ensure offspring values stay within bounds [0, 1]
        offspring[i] = np.clip(offspring[i], 0.0, 1.0)
    
    return offspring