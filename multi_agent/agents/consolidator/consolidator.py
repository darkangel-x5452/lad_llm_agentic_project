from ollama import chat


class ConsolidatorAgent:
    def __init__(self):
        pass

    def handle_result(self, prompt: str, answer: str):
        response = chat(
            model='llama3.2:3b',
            messages=[
                {"role": "system", "content": "You are an agent expert result summariser and been to summarise the results of an answer for a prompt. Given the result, summarise it into a nice structure and format that aligns with the original prompt."},
                {"role": "user", "content": "Write a summary for the given answer for the original prompt question. Prompt question:\n" + prompt + "\nAnswer:\n" + answer}
            ]
        )

        print(response['message']['content'])
        resp = response['message']['content']
        return resp
