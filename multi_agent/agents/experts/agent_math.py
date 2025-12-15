from ollama import chat
from multi_agent.agents.base_agent import BaseAgent

class MathAgent(BaseAgent):
    def __init__(self):
        super().__init__("MathAgent")

    def handle_task(self, task):
        response = chat(
            model='llama3.2:3b',
            messages=[
                {"role": "system", "content": "You are an agent expert mathematician and been asked to explain mathematic questions like a teacher. Provide clear explanation as a mathematics teacher."},
                {"role": "user", "content": "Explain following prompt:\n" + task}
            ]
        )
        resp = response['message']['content']
        return resp
