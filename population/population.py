from typing import List, Dict
from task import AbstractTask, mapping
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
				 size,
				 lst_solvers: List[Solver],
				 mem: Memory):
		self.lst_tasks: List[AbstractTask] = lst_tasks
		self.lst_task_names = [task.task_name for task in self.lst_tasks]
		self.dict_tasks: Dict[str, AbstractTask] = {}
		for task in self.lst_tasks:
			self.dict_tasks[task.task_name] = task

		self.dict_taskpopulations: Dict[str, TaskPopulation] = {}
		self.size = size
		self.num_solvers = len(lst_solvers)
		self.lst_solvers = lst_solvers
		self.mem = mem
		self.indi_dim = max([task.dim for task in self.lst_tasks])

		self.dict_best_fitness : Dict[str, float] = {}

		for i in range(len(self.lst_tasks)):
			task_name = self.lst_tasks[i].task_name
			self.dict_taskpopulations[task_name] = TaskPopulation(task=self.lst_tasks[i], 
																 lst_solvers=self.lst_solvers,
																 size=int(self.size / len(self.lst_tasks)),
																 mem=self.mem,
																 dim = self.indi_dim)
		
	
	def evolve(self, gen : int):
		for task_name in self.lst_task_names:
			self.dict_taskpopulations[task_name].evolve(gen=gen)
			self.dict_best_fitness[task_name] = self.dict_taskpopulations[task_name].get_best_fitness()

			if gen % self.mem.memory_size == 0:
				for solver in self.lst_solvers:
					self.mem.update_p_value(task_name=task_name, solver_id=solver.id, generation=gen)

	def knowledge_transfer(self, k : int):
		# Construct the transfer pool
		transfer_pool : Dict[str, List[Individual]] = {}
		for task_name in self.lst_task_names:
			transfer_pool[task_name] = self.dict_taskpopulations[task_name].remove_individuals(k=k)

		for task_name in self.lst_task_names:
			other_task_names = [tn for tn in self.lst_task_names if tn != task_name]
			for indi in transfer_pool[task_name]:
				while True:
					target_task_name = random.choice(other_task_names)
					if self.dict_taskpopulations[target_task_name].is_full():
						continue
					self.dict_taskpopulations[target_task_name].add_individual(indi=mapping(indi, 
																							src_task=self.dict_tasks[task_name], 
																							target_task=self.dict_tasks[target_task_name]))
					break
	
	def update_solvers(self, lst_solvers: List[Solver]):
		self.lst_solvers = lst_solvers
		for task_name in self.lst_task_names:
			self.dict_taskpopulations[task_name].update_solvers(self.lst_solvers)
		
		self.mem.restart([solver.id for solver in self.lst_solvers])

	def load_pop(self, path:str):
		# TODO implement this if have time
		pass

	def save_pop(self, path:str):
		# TODO implement this if have time
		pass

	
