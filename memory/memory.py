from typing import List, Dict
import pandas as pd

# TODO: Optimize these functions
class Memory():
	def __init__(self, memory_size: int = 2):
		self.memory_size = memory_size

		# Num success and num failure of each generation
		self.data = pd.DataFrame(columns=["solver_id", "generation", "num_success", "num_failure"])
		
		# Probability of success
		self.p_data = pd.DataFrame(columns=["solver_id", "p"])

		self.lst_solver_ids = []
		self.lst_best_solver_ids = []

		# self.restart(self.lst_solver_ids)

	def restart(self, lst_solver_ids: List[str]):
		self.data = pd.DataFrame(columns=self.data.columns)
		self.p_data = pd.DataFrame(columns=self.p_data.columns)

		self.lst_solver_ids = lst_solver_ids

		for solver_id in lst_solver_ids:
			self.set_value(solver_id, 0, 0, 0)
			self.set_p_value(solver_id, 1.0 / len(self.lst_solver_ids)) # Every solver get an equal chance at the beginning

	def set_p_value(self, solver_id: str, p: float):
		mask = ((self.p_data["solver_id"] == solver_id))
		if mask.any():
			self.p_data.loc[mask, "p"] = p
		else:
			new_row = {
				"solver_id": solver_id,
				"p": p
			}
			self.p_data = pd.concat([self.p_data, pd.DataFrame([new_row])], ignore_index=True)

	def set_value(self, solver_id: str, generation: int, num_success: int, num_failure: int) :
		mask = (
			(self.data["solver_id"] == solver_id) &
			(self.data["generation"] == generation)
		)
		if mask.any():
			self.data.loc[mask, ["num_success", "num_failure"]] = [num_success, num_failure]
		else:
			new_row = {
				"solver_id": solver_id,
				"generation": generation,
				"num_success": num_success,
				"num_failure": num_failure
			}
			self.data = pd.concat([self.data, pd.DataFrame([new_row])], ignore_index=True)

	def get_p_value(self, solver_id):
		row = self.p_data[(self.p_data["solver_id"] == solver_id)]
		if row.empty:
			print(f'[ERROR] Solver {solver_id}\'s p value does not exist.')
			return 0
		return row["p"].iloc[0]

	def get_value(self, solver_id, generation):
		row = self.data[
			(self.data["solver_id"] == solver_id) &
			(self.data["generation"] == generation)
		]
		if row.empty:
			return None
		return row[["num_success", "num_failure"]].iloc[0].to_dict()

	def check_exist(self, solver_id, generation) -> bool:
		mask = (
			(self.data["solver_id"] == solver_id) &
			(self.data["generation"] == generation)
		)
		return mask.any()

	def get_num_success(self, solver_id, generation) -> int:
		if self.check_exist(solver_id, generation):
			return self.get_value(solver_id, generation)['num_success']
		else:
			print(f'[ERROR] Solver {solver_id}, generation {generation} does not exists')

	def get_num_failure(self, solver_id, generation) -> int:
		if self.check_exist(solver_id, generation):
			return self.get_value(solver_id, generation)['num_failure']
		else:
			print(f'[ERROR] Solver {solver_id}, generation {generation} does not exists')
	
	def get_best_solver_id(self) -> str:
		print("[*] Getting best solver id ...")
		best_solver_id = self.lst_solver_ids[0]
		best_p_value = self.get_p_value(best_solver_id)

		for solver_id in self.lst_solver_ids:
			p_value = self.get_p_value(solver_id)
			if p_value > best_p_value:
				best_solver_id, best_p_value = solver_id, p_value
		print(f'[*] Best solver id: {best_solver_id} with p value: {best_p_value}')
		return best_solver_id

	def get_worst_solver_id(self) -> str:
		print("[*] Getting worst solver id ...")
		worst_solver_id = self.lst_solver_ids[0]
		worst_p_value = self.get_p_value(worst_solver_id)

		for solver_id in self.lst_solver_ids:
			p_value = self.get_p_value(solver_id)
			if p_value < worst_p_value:
				worst_solver_id, worst_p_value = solver_id, p_value
		print(f'[*] Worst solver id: {worst_solver_id} with p value: {worst_p_value}')
		return worst_solver_id

	def get_success_rate(self, solver_id, generation, eps=1e-3):
		mask = (
			(self.data["solver_id"] == solver_id) & 
			(self.data["generation"].between(generation - self.memory_size + 1, generation))
 		)
		success_cnt = self.data.loc[mask, "num_success"].sum()
		failure_cnt = self.data.loc[mask, "num_failure"].sum()

		success_rate = success_cnt / (success_cnt + failure_cnt) + eps 
		return success_rate
		
	def update_p_value(self, solver_id, generation, sigma=0.5):
		upper = self.get_success_rate(solver_id, generation) + sigma * self.get_p_value(solver_id)
		lower = 0
		for _solver_id in self.lst_solver_ids:
			lower += self.get_success_rate(_solver_id, generation) + sigma * self.get_p_value(_solver_id)
		new_p_value = upper / lower
		self.set_p_value(solver_id, new_p_value)
