import os
import json

def get_p_value(task_name: str, solver_id: str) -> float:
    BASE_DIR = os.path.dirname(__file__)
    file_path = os.path.join(BASE_DIR, "data", solver_id + '.json')

    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data[task_name]
    else:
        print('[ERROR] Solver\'s id does not exist')
        return 0

def update_p_values():
    pass

def reset_p_values():
    pass
