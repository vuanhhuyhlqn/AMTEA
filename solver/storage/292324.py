import numpy as np

def crossover(parent1, parent2):
    dim = len(parent1)
    offspring = np.zeros(dim)
    
    for i in range(dim):
        distance = abs(parent1[i] - parent2[i])
        if distance < 1e-6:  # Prevent division by zero
            alpha = np.random.rand()
        else:
            alpha = 0.5 * (1 + (1 - abs(parent1[i] - parent2[i])) / (1 - min(parent1[i], parent2[i])))
        
        blend_value = 0.5 * (parent1[i] + parent2[i])
        cmin = min(parent1[i], parent2[i])
        cmax = max(parent1[i], parent2[i])
        I = cmax - cmin
        lower = cmin - 0.5 * I
        upper = cmax + 0.5 * I
        random_value = np.random.uniform(lower, upper)

        offspring[i] = alpha * blend_value + (1 - alpha) * random_value
        offspring[i] = np.clip(offspring[i], 0.0, 1.0)  # Ensure bounds

    return offspring