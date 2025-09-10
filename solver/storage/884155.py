import numpy as np

def crossover(parent1, parent2, eta=20, alpha=0.5):
    dim = len(parent1)
    offspring = np.zeros(dim)
    
    # Simulated Binary Crossover (SBX) step
    for i in range(dim):
        u = np.random.rand()
        if u <= 0.5:
            beta = (2 * u) ** (1 / (eta + 1))
        else:
            beta = (1 / (2 * (1 - u))) ** (1 / (eta + 1))
        sbx_value = 0.5 * ((1 + beta) * parent1[i] + (1 - beta) * parent2[i])
        sbx_value = np.clip(sbx_value, 0.0, 1.0)

        # BLX-α refinement step
        cmin = min(parent1[i], parent2[i])
        cmax = max(parent1[i], parent2[i])
        I = cmax - cmin
        lower = cmin - alpha * I
        upper = cmax + alpha * I
        offspring[i] = np.random.uniform(lower, upper)
        
        # Select the best between SBX value or refined BLX-α value
        offspring[i] = np.clip(offspring[i], 0.0, 1.0)  # Ensure bounds
        offspring[i] = (offspring[i] + sbx_value) / 2  # Combine both approaches

    return offspring