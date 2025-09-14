class AbstractModel:
	def __init__(self, model: str, client):
		self.model = model
		self.client = client

	def get_response(self, prompt_content: str):
		pass