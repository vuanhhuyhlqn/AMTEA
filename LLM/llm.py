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
        
        id = save_code(code_all)
        print(f'Solver initialized with id: {id}')
        return [id, algorithm]