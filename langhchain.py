import openai

class OpenAIChat:
    def __init__(self, api_key, temperature=0.7):
        self.api_key = api_key
        self.temperature = temperature
        self.max_tokens = 4096  # OpenAI maximum is 4096

    def generate_response(self, prompt):
        openai.api_key = self.api_key
        response = openai.Completion.create(
            engine="text-davinci-003",  # Replace with the desired language model
            prompt=prompt,
            temperature=self.temperature,
            max_tokens=self.max_tokens,
            stop=["\n"]
        )
        return response.choices[0].text.strip()
