from typing import List, Dict
import random
from task import AbstractTask
from subpopulation import SubPopulation
from indi import Individual
from solver import Solver
from memory import get_p_value
import numpy as np

class TaskPopulation:
    def __init__(self, task : AbstractTask, size : int, lst_solvers: List[Solver]):
        self.task = task
        self.size = size
        self.lst_solvers = lst_solvers
        self.num_solvers = len(self.lst_solvers)
        

        self.lst_indis : List[Individual] = []
        while len(self.lst_indis) < self.size:
            self.lst_indis.append(Individual(self.task.dim))

    def evolve(self):
        # divide lst_indis into subpopulation
        # current_median_fitness : float = self.get_median_fitness()

        dict_subpopulations : Dict[str, SubPopulation] = {}
        lst_p_values : List[float] = []

        for solver in self.lst_solvers:
            dict_subpopulations[solver.id] = SubPopulation(self.task, solver)
            lst_p_values.append(get_p_value(self.task.task_name, solver.id))

        solver_ids : List[str] = [solver.id for solver in self.lst_solvers]

        for indi in self.lst_indis:
            chosen_solver_id = random.choices(solver_ids, weights=lst_p_values, k=1)[0]

            dict_subpopulations[chosen_solver_id].add_individual(indi)
        
        for solver_id in solver_ids:
            dict_subpopulations[solver_id].evolve()
            #TODO: update success/failure memory


    def get_median_fitness(self) -> float:
        #TODO code this function
        return 100
    

    def remove_solvers(self, solver_ids):
        pass

    def add_solvers(self, solver_ids):
        pass


        


        