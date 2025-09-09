
class InterfaceAPI:
    def __init__(self, api_endpoint, api_key, model_LLM):
        self.api_endpoint = api_endpoint
        self.api_key = api_key
        self.client = model_LLM

    def get_response(self, prompt_content, temp=1.):
        response = self.client.chat_completion(1, [{"role": "user", "content": prompt_content}], temperature=temp)
        ret = response[0].message.content
        return ret