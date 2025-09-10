import numpy as np

def crossover(parent1, parent2, alpha=0.5, n_candidates=5):
    dim = len(parent1)
    offspring_candidates = []
    
    for _ in range(n_candidates):
        offspring = np.zeros(dim)
        for i in range(dim):
            cmin = min(parent1[i], parent2[i])
            cmax = max(parent1[i], parent2[i])
            I = cmax - cmin
            lower = cmin - alpha * I
            upper = cmax + alpha * I
            candidate_value = np.random.uniform(lower, upper)
            offspring[i] = np.clip(candidate_value, 0.0, 1.0)  # Ensure bounds
        offspring_candidates.append(offspring)
    
    # Select the best candidate (for this example, just return the first one)
    best_offspring = offspring_candidates[0]
    
    return offspring