from abstract import AbstractModel
from openai import OpenAI

class GPTModel(AbstractModel):
    def __init__(self, model: str, api_key: str):
        self.client = OpenAI(api_key=api_key)
        self.model = model

    def get_response(self, prompt_content, temperature=1.0):
        print('[*] Waiting for LLM response')
        chat_completion = self.client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt_content,
                }
            ],
            model=self.model,
            temperature=temperature
        )
        print('[*] Response received')
        return chat_completion.choices[0].message.content