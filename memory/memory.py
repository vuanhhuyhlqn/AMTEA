from typing import List, Dict
import pandas as pd

class Memory():
	def __init__(self, memory_size: int = 5):
		self.memory_size = memory_size
		self.data = pd.DataFrame(columns=["task_name", "solver_id", "generation", "num_success", "num_failure"])
	
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
	
	def get_success_rate(self, task_name, solver_id):
		#TODO: implement this
		pass