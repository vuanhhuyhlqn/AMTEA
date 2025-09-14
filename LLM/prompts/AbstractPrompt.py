from utils.utils import get_prompt

class AbstractPrompt:
    def __init__(self, prompt_name: str):
        self.prompt_name = prompt_name
        
    def get_prompt(self):
        return get_prompt(self.prompt_name)