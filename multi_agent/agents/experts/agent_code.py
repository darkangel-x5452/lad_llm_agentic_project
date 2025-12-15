from ollama import chat
from multi_agent.agents.base_agent import BaseAgent

class CodeAgent(BaseAgent):
    def __init__(self):
        super().__init__("CodeAgent")

    def handle_task(self, task):
        response = chat(
            model='llama3.2:3b',
            messages=[
                {"role": "system", "content": "You are an agent expert computer science coder and been asked to code in the specified language. Provide precise code and code explanation only."},
                {"role": "user", "content": "Write code for the following prompt:\n" + task}
            ]
        )

        resp = response['message']['content']
        return resp
