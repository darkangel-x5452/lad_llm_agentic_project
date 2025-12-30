import asyncio
from ollama import chat
import json
from memorisation_context.long_term import SemanticMemory
from memorisation_context.short_term import ShortTermMemory
from multi_agent.agents.base_agent import BaseAgent
from multi_agent.agents.consolidator.consolidator import ConsolidatorAgent
from multi_agent.agents.experts.agent_text import TextAgent
from multi_agent.agents.experts.agent_math import MathAgent
from multi_agent.agents.experts.agent_code import CodeAgent
from multi_agent.agents.experts.agent_weather import WeatherAgent

class OrchestratorAgent:
    def __init__(self):
        self.agents: dict[str, BaseAgent] = {
            "text": TextAgent(),
            "math": MathAgent(),
            "code": CodeAgent(),
            "weather": WeatherAgent(),
        }
        self.short_memory = ShortTermMemory()
        self.semantic_memory = SemanticMemory()

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

        categories: dict[str, str] = {_cat: " ".join(_question) for _cat, _question in categories.items() if _cat in category_options}
        return categories
    
    def add_recent_context(self, cat_prompt: str):
        self.short_memory.add("user", cat_prompt)

    def get_recent_context(self, prompt: str) -> str:
        recent_prompt = self.short_memory.get_context()

        new_prompt = f"{prompt}\nRecent Context:\n{recent_prompt}"

        return new_prompt

    def add_persist_context(self, prompt: str):
        self.semantic_memory.add(prompt)

    def get_persist_context(self, prompt: str) -> str:
        relevant_docs = self.semantic_memory.query(prompt)
        context = "\n".join(d["text"] for d in relevant_docs)

        new_prompt = f"{prompt}\nSemantic Context:\n{context}"
        return new_prompt

    async def handle_prompt(self, prompt):
        categories = self.categorize_task(prompt)
        results = []
        for cat in categories:
            agent = self.agents[cat]
            prompt_task = self.get_recent_context(categories[cat])
            prompt_task = self.get_persist_context(prompt_task)

            if cat == "weather":
                # res = asyncio.run(agent.handle_task(categories[cat]))
                res = await agent.handle_task(prompt_task)
            else:
                res = agent.handle_task(prompt_task)
            results.append(res)
        # Combine results into summary
        summary = "\n".join(results)

        ca = ConsolidatorAgent()
        summary = ca.handle_result(prompt, summary)
        self.add_recent_context(prompt)
        self.add_persist_context(summary)

        return summary

