import numpy as np

def crossover(parent1, parent2):
    dim = len(parent1)
    similarity = np.mean(np.abs(parent1 - parent2))
    alpha = 1 - np.clip(similarity, 0, 1)  # Adjust alpha based on similarity
    offspring = alpha * parent1 + (1 - alpha) * parent2
    offspring = np.clip(offspring, 0.0, 1.0)
    return offspring