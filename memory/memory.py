from typing import List, Dict
import pandas as pd

class Memory():
	def __init__(self, lst_task_names: List[str], memory_size: int = 2):
		self.memory_size = memory_size

		# Num success and num failure of each generation
		self.data = pd.DataFrame(columns=["task_name", "solver_id", "generation", "num_success", "num_failure"])
		
		# Probability of success
		self.p_data = pd.DataFrame(columns=["task_name", "solver_id", "p"])

		self.lst_task_names = lst_task_names
		self.lst_solver_ids = []

		# self.restart(self.lst_solver_ids)

	def restart(self, lst_solver_ids: List[str]):
		self.data = pd.DataFrame(columns=self.data.columns)
		self.p_data = pd.DataFrame(columns=self.p_data.columns)

		self.lst_solver_ids = lst_solver_ids

		for task_name in self.lst_task_names:
			for solver_id in lst_solver_ids:
				self.set_value(task_name, solver_id, 0, 0, 0)
				self.set_p_value(task_name, solver_id, 1.0 / len(self.lst_solver_ids)) # Every solver get an equal chance at the beginning

	def set_p_value(self, task_name: str, solver_id: str, p: float):
		mask = (
			(self.p_data["task_name"] == task_name) &
			(self.p_data["solver_id"] == solver_id)
		)
		if mask.any():
			self.p_data.loc[mask, "p"] = p
		else:
			new_row = {
				"task_name": task_name,
				"solver_id": solver_id,
				"p": p
			}
			self.p_data = pd.concat([self.p_data, pd.DataFrame([new_row])], ignore_index=True)

	def set_value(self, task_name: str, solver_id: str, generation: int, num_success: int, num_failure: int) :
		mask = (
			(self.data["task_name"] == task_name) &
			(self.data["solver_id"] == solver_id) &
			(self.data["generation"] == generation)
		)
		if mask.any():
			self.data.loc[mask, ["num_success", "num_failure"]] = [num_success, num_failure]
		else:
			new_row = {
				"task_name": task_name,
				"solver_id": solver_id,
				"generation": generation,
				"num_success": num_success,
				"num_failure": num_failure
			}
			self.data = pd.concat([self.data, pd.DataFrame([new_row])], ignore_index=True)

	def get_p_value(self, task_name, solver_id):
		row = self.p_data[
			(self.p_data["task_name"] == task_name) &
			(self.p_data["solver_id"] == solver_id)
		]
		if row.empty:
			print(f'[ERROR] Task {task_name}, solver {solver_id}\'s p value does not exist.')
			return 0
		return row["p"].iloc[0]

	def get_avg_p_value(self, solver_id : str) -> float:
		"""
		Get the average p value of solver across all tasks
		"""
		avg_p = self.p_data.loc[self.p_data["solver_id"] == solver_id, "p"].mean()
		return avg_p

	def get_value(self, task_name, solver_id, generation):
		row = self.data[
			(self.data["task_name"] == task_name) &
			(self.data["solver_id"] == solver_id) &
			(self.data["generation"] == generation)
		]
		if row.empty:
			return None
		return row[["num_success", "num_failure"]].iloc[0].to_dict()

	def check_exist(self, task_name, solver_id, generation) -> bool:
		mask = (
			(self.data["task_name"] == task_name) &
			(self.data["solver_id"] == solver_id) &
			(self.data["generation"] == generation)
		)
		return mask.any()

	def get_num_success(self, task_name, solver_id, generation) -> int:
		if self.check_exist(task_name, solver_id, generation):
			return self.get_value(task_name, solver_id, generation)['num_success']
		else:
			print(f'[ERROR] Task {task_name}, solver {solver_id}, generation {generation} does not exists')

	def get_num_failure(self, task_name, solver_id, generation) -> int:
		if self.check_exist(task_name, solver_id, generation):
			return self.get_value(task_name, solver_id, generation)['num_failure']
		else:
			print(f'[ERROR] Task {task_name}, solver {solver_id}, generation {generation} does not exists')
	
	def get_success_rate(self, task_name, solver_id, generation, eps=1e-3):
		success_cnt = 0
		failure_cnt = 0
		for i in range(generation - self.memory_size + 1, generation + 1):
			success_cnt += self.get_num_success(task_name, solver_id, i)
			failure_cnt += self.get_num_failure(task_name, solver_id, i)

		# print(f'Task {task_name}, solver {solver_id}, success_cnt: {success_cnt}, failure_cnt: {failure_cnt}')
		success_rate = success_cnt / (success_cnt + failure_cnt) + eps 
		return success_rate
		
	def update_p_value(self, task_name, solver_id, generation, sigma=0.5):
		upper = self.get_success_rate(task_name, solver_id, generation) + sigma * self.get_p_value(task_name, solver_id)
		lower = 0
		for _solver_id in self.lst_sover_ids:
			lower += self.get_success_rate(task_name, _solver_id, generation) + sigma * self.get_p_value(task_name, _solver_id)
		new_p_value = upper / lower
		self.set_p_value(task_name, solver_id, new_p_value)
