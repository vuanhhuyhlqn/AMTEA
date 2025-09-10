import numpy as np

def crossover(parent1, parent2):
    dim = len(parent1)
    crossover_point1 = np.random.randint(0, dim)
    crossover_point2 = np.random.randint(0, dim)
    
    if crossover_point1 > crossover_point2:
        crossover_point1, crossover_point2 = crossover_point2, crossover_point1
        
    offspring = np.copy(parent1)
    offspring[crossover_point1:crossover_point2] = parent2[crossover_point1:crossover_point2]
    offspring = np.clip(offspring, 0.0, 1.0)
    
    return offspring