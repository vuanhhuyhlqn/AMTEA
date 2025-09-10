import numpy as np
def crossover(parent1, parent2, alpha=None, eta=20):
    dim = len(parent1)
    offspring = np.zeros(dim)
    if alpha is None:
        alpha = np.random.rand()
    for i in range(dim):
        u = np.random.rand()
        if u <= 0.5:
            beta = (2*u)**(1/(eta+1))
        else:
            beta = (1/(2*(1-u)))**(1/(eta+1))
        offspring[i] = alpha * (0.5*((1+beta)*parent1[i] + (1-beta)*parent2[i])) + (1 - alpha) * parent1[i]
        offspring[i] = np.clip(offspring[i], 0.0, 1.0)
    return offspring