import sys
import os
import numpy as np
import importlib.util

def main():
    if len(sys.argv) < 2:
        print('Missing solver id')
        sys.exit(1)
    solver_id = sys.argv[1]
    
    solver_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'cache', 'solvers', f'{solver_id}.py'))
    
    spec = importlib.util.spec_from_file_location(f'solver_{solver_id}', solver_path)
    solver_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(solver_module)
    
    solve_func = getattr(solver_module, 'generation')
    
    temp_file = os.path.join(os.path.dirname(__file__), 'temp', 'temp_parents.npy')
    operands = np.load(temp_file, allow_pickle=True)
    
    result = solve_func(*operands)
    
    output_file = os.path.join(os.path.dirname(__file__), 'temp', 'output.npy')
    np.save(output_file, result, allow_pickle=True)

if __name__ == '__main__':
    main()
