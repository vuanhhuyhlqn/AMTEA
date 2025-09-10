import numpy as np

def crossover(parent1, parent2, fitness1, fitness2):
    dim = len(parent1)
    alpha = fitness1 / (fitness1 + fitness2)  # Adaptive blending ratio based on fitness
    offspring = np.zeros(dim)
    
    for i in range(dim):
        blend_part = alpha * parent1[i] + (1 - alpha) * parent2[i]
        # Random perturbation to enhance genetic diversity
        perturbation = np.random.uniform(-0.1, 0.1)
        offspring[i] = np.clip(blend_part + perturbation, 0.0, 1.0)
        
    return offspring