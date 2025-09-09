from typing import List, Dict
import pandas as pd

class Memory():
    def __init__(self, memory_size: int):
        self.memory_size = memory_size
        self.data = pd.DataFrame(columns=["task_name", "solver_id", "generation", "num_success", "num_failure"])
        


