from ollama import chat
from multi_agent.agents.base_agent import BaseAgent

class TextAgent(BaseAgent):
    def __init__(self):
        super().__init__("TextAgent")

    def handle_task(self, task):
        response = chat(
            model='llama3.2:3b',
            messages=[
                {"role": "system", "content": "You are an agent expert explainer and been asked a question. Provide an explanation only like a teacher to a student."},
                {"role": "user", "content": "Write explanation for the following prompt:\n" + task}
            ]
        )

        resp = response['message']['content']
        return resp