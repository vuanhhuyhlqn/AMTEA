class Paras():
    def __init__(self):
        #####################
        ### LLM settings  ###
        #####################
        self.llm_api_endpoint = "chat.openai.com"
        self.llm_model = "gpt-4o-mini"
        
    def set_paras(self, *args, **kwargs):
    # Map paras
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
                
if __name__ == "__main__":
    # Create an instance of the Paras class
    paras_instance = Paras()