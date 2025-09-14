from typing import List, Dict
from task import AbstractTask
from indi import Individual
from taskpopulation import TaskPopulation
from subpopulation import SubPopulation
from solver import Solver
from memory import Memory
import random
import numpy as np

class Population:
	def __init__(self, 
				 lst_tasks: List[AbstractTask], 
				 size: int,
				 memory_size : int):
		self.lst_tasks: List[AbstractTask] = lst_tasks
		self.lst_task_names = [task.task_name for task in self.lst_tasks]
		self.dict_tasks: Dict[str, AbstractTask] = {}
		for task in self.lst_tasks:
			self.dict_tasks[task.task_name] = task

		self.dict_taskpopulations: Dict[str, TaskPopulation] = {}
		self.size = size
		self.memory_size = memory_size
		self.indi_dim = max([task.dim for task in self.lst_tasks])

		self.dict_best_fitness : Dict[str, float] = {}

		for i in range(len(self.lst_tasks)):
			task_name = self.lst_tasks[i].task_name
			self.dict_taskpopulations[task_name] = TaskPopulation(task=self.lst_tasks[i], 
																 size=int(self.size / len(self.lst_tasks)),
																 memory_size=self.memory_size,
																 dim = self.indi_dim)

	def evolve(self, gen : int, lp : int = 10, tgap : int = 10, k : int = 5):
		for task_name in self.lst_task_names:

			parents = [indi for indi in self.dict_taskpopulations[task_name].lst_indis]
			if gen % lp <= lp - self.memory_size and gen % tgap == 0:
				print('[*] KNOWLEDGE TRANSFER')
				replace_idx = np.random.randint(0, len(parents), size=k)
				transfer_pool = self.get_transfer_pool(task_name, k)
				for i, replace_id in enumerate(replace_idx):
					parents[replace_id] = transfer_pool[i]

			self.dict_taskpopulations[task_name].evolve(gen=gen, parents=parents)
			self.dict_best_fitness[task_name] = self.dict_taskpopulations[task_name].get_best_fitness()

			if gen % lp == 0:
				for solver in self.dict_taskpopulations[task_name].lst_solvers:
					self.dict_taskpopulations[task_name].mem.update_p_value(solver_id=solver.id, generation=gen)

	def get_transfer_pool(self, task_name, k : int):
		transfer_pool : List[Individual] = []
		for _ in range(k):
			tmp_task_name = random.choice([tn for tn in self.lst_task_names if tn != task_name])
			indi = self.dict_taskpopulations[tmp_task_name].get_random_individuals(1)[0]
			transfer_pool.append(indi)
		return transfer_pool
	
