import numpy as np

def crossover(parent1, parent2, eta=20):
    dim = len(parent1)
    offspring = np.zeros(dim)
    
    for i in range(dim):
        # Differential Evolution inspired mutation step
        mutant = parent1[i] + np.random.rand() * (parent2[i] - parent1[i])
        
        # Simulated Binary Crossover (SBX) for blending
        u = np.random.rand()
        if u <= 0.5:
            beta = (2 * u) ** (1 / (eta + 1))
        else:
            beta = (1 / (2 * (1 - u))) ** (1 / (eta + 1))
        sbx_value = 0.5 * ((1 + beta) * parent1[i] + (1 - beta) * parent2[i])
        
        # Weighted blend between mutant and SBX value
        alpha = np.random.rand()  # Random blend factor
        offspring[i] = alpha * mutant + (1 - alpha) * sbx_value
        
        # Ensuring offspring bounds
        offspring[i] = np.clip(offspring[i], 0.0, 1.0)

    return offspring