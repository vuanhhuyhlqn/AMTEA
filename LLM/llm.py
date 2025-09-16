import re
from utils.utils import *
from .llm_models import *
from .prompts import *

class LLM():
    
    def __init__(self, model: AbstractModel):
        self.model = model
    
    def init_solver(self):
        prompt_content = InitPrompt().get_prompt()
        [id, algorithm] = self._get_alg(prompt_content)
        print(algorithm)
        print(f'Solver initialized with id: {id}')
        return [id, algorithm]
    
    def update_solver(self, good_solver_history, bad_solver_history, alpha):
        prompt_content = UpdatePrompt(good_solver_history, bad_solver_history, alpha).get_prompt()
        [id, algorithm] = self._get_alg(prompt_content)
        print(algorithm)
        print(f'New solver updated with id: {id}')
        return [id, algorithm]
    
    def _get_alg(self, prompt_content):

        response = self.model.get_response(prompt_content)
        # print("LLM response:")
        # print(response)

        desc_match = re.search(r"\{(.*?)\}", response, re.DOTALL)
        algorithm = desc_match.group(1).strip() if desc_match else ""

        code_match = re.search(r"```(?:python)?\s*(.*?)```", response, re.DOTALL)
        if code_match:
            code = code_match.group(1).strip()
        else:
            code_match2 = re.search(r"(import[\s\S]*)", response)
            if code_match2:
                code = code_match2.group(1).strip()
            else:
                code_match3 = re.search(r"(def[\s\S]*)", response)
                code = code_match3.group(1).strip() if code_match3 else ""

        n_retry = 1
        while (not algorithm or not code) and n_retry <= 3:
            print("Error: algorithm or code not identified, retrying ...")
            response = self.interface_llm.get_response(prompt_content)

            desc_match = re.search(r"\{(.*?)\}", response, re.DOTALL)
            algorithm = desc_match.group(1).strip() if desc_match else ""

            code_match = re.search(r"```(?:python)?\s*(.*?)```", response, re.DOTALL)
            if code_match:
                code = code_match.group(1).strip()
            else:
                code_match2 = re.search(r"(import[\s\S]*)", response)
                if code_match2:
                    code = code_match2.group(1).strip()
                else:
                    code_match3 = re.search(r"(def[\s\S]*)", response)
                    code = code_match3.group(1).strip() if code_match3 else ""

            n_retry += 1
        
        id = save_code(code)

        return [id, algorithm]