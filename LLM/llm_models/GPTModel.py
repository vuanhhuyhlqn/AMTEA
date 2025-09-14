from .AbstractModel import AbstractModel

class GPTModel(AbstractModel):
    def __init__(self, model, client):
        super().__init__(model, client)
        
    def get_response(self, prompt_content: str):
        response = self.client.responses.create(
            model = self.model,
            input = prompt_content
        )
        return response.output_text