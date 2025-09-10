import re
import time
from .interface_LLM import InterfaceAPI as InterfaceLLM
from utils.utils import *

input = lambda: ...

class LLM():
    
    def __init__(self, api_endpoint, api_key, model_LLM):
        # set LLMs
        self.api_endpoint = api_endpoint
        self.api_key = api_key
        self.model_LLM = model_LLM
        self.interface_llm = InterfaceLLM(self.api_endpoint, self.api_key, self.model_LLM)
        
    def get_prompt_init(self):
        prompt_content = get_prompt('init')
        return prompt_content
    
    def get_prompt_update(self, good_solver_history, bad_solver_history):
        prompt_parts = []
        prompt_parts.append(
            "I am solving optimization problems using evolutionary algorithms.\n"
            "The goal is to design crossover solvers that take two parent solutions and produce one offspring solution.\n"
        )

        prompt_parts.append("I have a list of well-performing solvers with their descriptions and Python code implementations as follows:\n")
        prompt_parts.append("**Good solvers:**\n")
        for idx, solver in enumerate(good_solver_history, 1):
            prompt_parts.append(f"No.{idx} solver’s description and its code:\n"
                                f"# Its Description\n{{{solver.algorithm}}}\n"
                                "# Its Python Code Implementation of a Function\n"
                                f"{get_code(solver.id)}\n")

        if bad_solver_history:
            prompt_parts.append("\n**Poor solvers to avoid:**\n")
            for idx, solver in enumerate(bad_solver_history, 1):
                prompt_parts.append(f"No.{idx} poor solver’s description and its code:\n"
                                    f"# Its Description\n{{{solver.algorithm}}}\n"
                                    "# Its Python Code Implementation of a Function\n"
                                    f"{get_code(solver.id)}\n")

        prompt_parts.append(
            "\nPlease create a new crossover solver that takes inspiration from the well-performing solvers but avoids the weaknesses and design patterns of the poor-performing solvers.\n"
            "The new solver should aim for strong performance on optimization tasks.\n\n"
            "First, describe the design idea and main steps of your solver in one sentence. "
            "The description must be inside a brace outside the code implementation.\n\n"
            "Next, implement it in Python as a function named `crossover`.\n\n"
            "This function should accept 2 inputs: `parent1` and `parent2`, both real-valued vectors.\n\n"
            "The function should return 1 output: `offspring`, a real-valued vector.\n\n"
            "The offspring must stay within the bounds [0, 1] for each variable.\n\n"
            "Do not give additional explanations."
        )

        return "\n".join(prompt_parts)
    
    def _get_alg(self, prompt_content):

        response = self.interface_llm.get_response(prompt_content)

        algorithm = re.search(r"\{(.*?)\}", response, re.DOTALL).group(1)
        if len(algorithm) == 0:
            if 'python' in response:
                algorithm = re.findall(r'^.*?(?=python)', response, re.DOTALL)
            elif 'import' in response:
                algorithm = re.findall(r'^.*?(?=import)', response, re.DOTALL)
            else:
                algorithm = re.findall(r'^.*?(?=def)', response, re.DOTALL)

        code = re.findall(r"import.*return", response, re.DOTALL)
        if len(code) == 0:
            code = re.findall(r"def.*return", response, re.DOTALL)

        n_retry = 1
        while (len(algorithm) == 0 or len(code) == 0):
            print("Error: algorithm or code not identified, wait 1 seconds and retrying ... ")

            response = self.interface_llm.get_response(prompt_content)

            algorithm = re.search(r"\{(.*?)\}", response, re.DOTALL).group(1)
            if len(algorithm) == 0:
                if 'python' in response:
                    algorithm = re.findall(r'^.*?(?=python)', response, re.DOTALL)
                elif 'import' in response:
                    algorithm = re.findall(r'^.*?(?=import)', response, re.DOTALL)
                else:
                    algorithm = re.findall(r'^.*?(?=def)', response, re.DOTALL)

            code = re.findall(r"import.*return", response, re.DOTALL)
            if len(code) == 0:
                code = re.findall(r"def.*return", response, re.DOTALL)

            if n_retry > 3:
                break
            n_retry += 1

        code = code[0]
        code_all = code + " " + ", ".join(['offspring'])

        return [code_all, algorithm]
    
    def init(self):
        print('Initializing solver ... ')
        prompt_content = self.get_prompt_init()

        [code_all, algorithm] = self._get_alg(prompt_content)
        print(algorithm)
        id = save_code(code_all)
        print(f'Solver initialized with id: {id}')
        return [id, algorithm]
    
    def update(self, good_solver_history, bad_solver_history):
        print('Updating solver ... ')
        prompt_content = self.get_prompt_update(good_solver_history, bad_solver_history)
        
        prompts_folder = 'LLM/prompts'
        os.makedirs(prompts_folder, exist_ok=True)
        prompt_file = os.path.join(prompts_folder, 'update.txt')
        with open(prompt_file, 'w', encoding='utf-8') as f:
            f.write(prompt_content)
        
        [code_all, algorithm] = self._get_alg(prompt_content)
        print(algorithm)
        
        id = save_code(code_all)
        print(f'New solver updated with id: {id}')
        return [id, algorithm]