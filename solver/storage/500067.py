import numpy as np

def crossover(parent1, parent2, eta=20, noise_strength=0.1):
    dim = len(parent1)
    offspring = np.zeros(dim)
    
    for i in range(dim):
        u = np.random.rand()
        # Simulated Binary Crossover (SBX) for gene blending
        if u <= 0.5:
            beta = (2 * u) ** (1 / (eta + 1))
        else:
            beta = (1 / (2 * (1 - u))) ** (1 / (eta + 1))
        sbx_value = 0.5 * ((1 + beta) * parent1[i] + (1 - beta) * parent2[i])

        # Generative mechanism with noise
        noise = np.random.uniform(-noise_strength, noise_strength)
        combined_value = (sbx_value + parent1[i] + parent2[i]) / 3 + noise
        
        # Clipping to ensure bounds
        offspring[i] = np.clip(combined_value, 0.0, 1.0)

    return offspring