import numpy as np

def crossover(parent1, parent2, eta=20):
    dim = len(parent1)
    offspring = np.zeros(dim)
    
    for i in range(dim):
        u = np.random.rand()
        # Simulated Binary Crossover (SBX) decision
        if u <= 0.7:  # 70% chance for SBX
            if u <= 0.5:
                beta = (2 * u) ** (1 / (eta + 1))
            else:
                beta = (1 / (2 * (1 - u))) ** (1 / (eta + 1))
            sbx_value = 0.5 * ((1 + beta) * parent1[i] + (1 - beta) * parent2[i])
            offspring[i] = np.clip(sbx_value, 0.0, 1.0)
        else:
            # Adaptive Random Sampling (ARS)
            alpha = np.random.rand()
            cmin = min(parent1[i], parent2[i])
            cmax = max(parent1[i], parent2[i])
            I = cmax - cmin
            lower = cmin - 0.3 * I  # 30% lower extension
            upper = cmax + 0.3 * I  # 30% upper extension
            offspring[i] = np.random.uniform(lower, upper)
            offspring[i] = np.clip(offspring[i], 0.0, 1.0)  # Ensure bounds

    return offspring