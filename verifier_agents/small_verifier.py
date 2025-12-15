import ollama
from typing import List, Dict

class CriticAgent:
    def __init__(self, model_name="llama3.2:3b"):
        self.model_name = model_name

    async def verify(self, expert_results: List[Dict]) -> Dict:
        """
        expert_results: List of dicts like:
        [{"agent": "WeatherAgent", "answer": "It will rain today in Sydney."}, ...]
        """

        # Flatten expert outputs
        combined_context = "\n".join(
            f"{res['agent']}: {res['answer']}" for res in expert_results
        )

        prompt = f"""
You are a Critic Agent.
You receive answers from multiple expert agents.
Tasks:
1. Check for factual correctness.
2. Identify contradictions.
3. Highlight missing evidence.
4. Suggest corrections if needed.

Expert outputs:
{combined_context}

Please return a JSON with:
- verified_answers: corrected or confirmed answers per agent
- issues: list of problems found
- overall_confidence: 0-1
"""
        response = ollama.chat(
            model=self.model_name,
            messages=[{"role": "user", "content": prompt}],
        )

        # You can parse structured output if Ollama returns JSON
        import json
        try:
            result = json.loads(response["message"]["content"])
        except json.JSONDecodeError:
            # fallback: return as plain text
            result = {"verified_answers": expert_results, "issues": ["JSON parse failed"], "overall_confidence": 0.5}

        return result
