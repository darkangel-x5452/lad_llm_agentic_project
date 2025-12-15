import asyncio
from ollama import chat
import json
from multi_agent.agents.consolidator.consolidator import ConsolidatorAgent
from multi_agent.agents.experts.agent_text import TextAgent
from multi_agent.agents.experts.agent_math import MathAgent
from multi_agent.agents.experts.agent_code import CodeAgent
from multi_agent.agents.experts.agent_weather import WeatherAgent

class OrchestratorAgent:
    def __init__(self):
        self.agents = {
            "text": TextAgent(),
            "math": MathAgent(),
            "code": CodeAgent(),
            "weather": WeatherAgent(),
            "weather": WeatherAgent(),
        }

    def categorize_task(self, prompt):
        category_options = list(self.agents.keys())
        response = chat(
            model='llama3.2:3b',
            messages=[
                {"role": "system", "content": f"You are a agent master that categorises prompts into these '{len(category_options)}' categories: '{json.dumps(category_options)}' and the categories will be sent to the expert agent."},
                {"role": "user", "content": f"""
                 You do not need to use all categories, just use the most relevents. 
                 The prompt can contain multiple questions so break up the prompt into it's relevant separate question(s).
                 Categorise the prompt question(s) into the relevant category or categories. 
                 Then assign each prompt sentence part to the most relevant category.
                 Output the result as a dictionary structure, where the category is key, and prompt sentence part(s) is value. 
                 Only output the json dictionary, it should start with {{ and and with }}.
                 Prompt: {prompt}"""
                 }
            ]
        )

        print(response['message']['content'])
        resp = response['message']['content']
        resp = resp.replace("\n", ' ')  # Ensure JSON compatibility
        resp = f"{resp} }}" if resp.strip().endswith("}") == False else resp  # Fix incomplete JSON

        """Simulate categorization. In real use, use LLM to categorize"""
        categories = json.loads(resp)  # Validate JSON

        categories = {_cat: " ".join(_question) for _cat, _question in categories.items() if _cat in category_options}
        return categories

    async def handle_prompt(self, prompt):
        categories = self.categorize_task(prompt)
        results = []
        for cat in categories:
            agent = self.agents[cat]
            if cat == "weather":
                # res = asyncio.run(agent.handle_task(categories[cat]))
                res = await agent.handle_task(categories[cat])
            else:
                res = agent.handle_task(prompt)
            results.append(res)
        # Combine results into summary
        summary = "\n".join(results)

        ca = ConsolidatorAgent()
        summary = ca.handle_result(prompt, summary)

        return summary

