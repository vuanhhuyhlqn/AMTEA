import numpy as np

def crossover(parent1, parent2):
    dim = len(parent1)
    offspring = np.zeros(dim)
    
    for i in range(dim):
        # Calculate range between parents
        delta = abs(parent1[i] - parent2[i])
        alpha = np.random.uniform(0.1, 0.9)  # Random blending factor
        
        # Calculate blended value
        blend_value = (1 - alpha) * parent1[i] + alpha * parent2[i]
        
        # Determine adjustment based on distance between parents
        if delta > 0.2:  # Larger distance allows for broader sampling
            lower = min(parent1[i], parent2[i]) - 0.5 * delta
            upper = max(parent1[i], parent2[i]) + 0.5 * delta
            offspring[i] = np.random.uniform(lower, upper)
        else:  # Smaller distance refines exploration
            offspring[i] = blend_value
        
        # Ensure offspring is within bounds
        offspring[i] = np.clip(offspring[i], 0.0, 1.0)

    return offspring