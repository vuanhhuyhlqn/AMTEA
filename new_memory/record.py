import pandas as pd

class Record:
	def __init__(self):
		self.data = pd.DataFrame(columns=["solver_id", "evaluation_count"])
	
	def add(self, solver_id : str, addition : int):
		mask = ((self.data["solver_id"] == solver_id))
		if mask.any():
			self.data.loc[mask, "evaluation_count"] += addition
		else:
			new_row = {
				"solver_id": solver_id,
				"evaluation_count": addition
			}
			self.data = pd.concat([self.data, pd.DataFrame([new_row])], ignore_index=True)
