from .AbstractModel import AbstractModel

class GeminiModel(AbstractModel):
    def __init__(self, model, client):
        super().__init__(model, client)
        
    def get_response(self, prompt_content: str):
        print("Generating response from Gemini model ... ")
        response = self.client.models.generate_content(
            model = self.model, 
            contents = prompt_content
        )
        return response.text