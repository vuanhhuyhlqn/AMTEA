import numpy as np

def crossover(parent1: np.ndarray, parent2: np.ndarray) -> np.ndarray:
    return (parent1 + parent2) / 2
