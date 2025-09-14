from .AbstractPrompt import AbstractPrompt

class InitPrompt(AbstractPrompt):
    def __init__(self, prompt_name = "init"):
        super().__init__(prompt_name)
        
    def get_prompt(self):
        return super().get_prompt()