import numpy as np

def crossover(parent1, parent2):
    dim = len(parent1)
    offspring = np.zeros(dim)

    for i in range(dim):
        alpha = np.random.rand()  # Random blending factor
        blend_value = 0.5 * (parent1[i] + parent2[i])
        if np.random.rand() < 0.7:  # 70% chance to use blending approach
            offspring[i] = alpha * blend_value + (1 - alpha) * parent1[i]  # Weighted blending
        else:
            offspring[i] = np.random.choice([parent1[i], parent2[i], blend_value])  # Randomly choose between parents or blend
        
        # Ensuring offspring bounds
        offspring[i] = np.clip(offspring[i], 0.0, 1.0)

    return offspring