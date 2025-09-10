import numpy as np

def crossover(parent1, parent2, eta=20):
    dim = len(parent1)
    offspring = np.zeros(dim)
    for i in range(dim):
        u = np.random.rand()
        if u <= 0.5:
            beta = (2 * u) ** (1 / (eta + 1))
        else:
            beta = (1 / (2 * (1 - u))) ** (1 / (eta + 1))
        sbx_part = 0.5 * ((1 + beta) * parent1[i] + (1 - beta) * parent2[i])
        
        alpha = np.random.rand()
        arith_part = alpha * parent1[i] + (1 - alpha) * parent2[i]
        
        offspring[i] = np.clip((sbx_part + arith_part) / 2, 0.0, 1.0)
        
    return offspring