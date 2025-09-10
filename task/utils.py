from indi import Individual
from task import AbstractTask
import numpy as np

def mapping(x: Individual, src_task: AbstractTask, target_task: AbstractTask) -> Individual:
    x_gene = x.gene
    x_upper_bound, x_lower_bound = src_task.upper_bound, src_task.lower_bound
    y_upper_bound, y_lower_bound = target_task.upper_bound, target_task.lower_bound
    y_gene = (x_gene - x_lower_bound) * (y_upper_bound - y_lower_bound) / (x_upper_bound - x_lower_bound) + y_lower_bound
    return Individual(x.dim, y_gene)

    
