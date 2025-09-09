import os
import json

#TODO: redesign memory format
def get_success_memory(task_name: str, solver_id: str) -> int:
    BASE_DIR = os.path.dirname(__file__)
    file_path = os.path.join(BASE_DIR, "data", solver_id + '.json')

    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data[task_name]["success"]
    else:
        print(f'[ERROR] Task {task_name}: Solver\'s id does not exist')
        return 0
    
def get_failure_memory(task_name: str, solver_id: str) -> int:
    BASE_DIR = os.path.dirname(__file__)
    file_path = os.path.join(BASE_DIR, "data", solver_id + '.json')

    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data[task_name]["failure"]
    else:
        print(f'[ERROR] Task {task_name}: Solver\'s id does not exist')
        return 0

def get_p_value(task_name: str, solver_id: str) -> float:
    pass

def update_p_values():
    pass

def reset_p_values():
    pass
