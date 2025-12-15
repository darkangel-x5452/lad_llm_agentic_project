import asyncio

class AgentWithMemory:
    def __init__(self):
        self.short_memory = ShortTermMemory()
        self.semantic_memory = SemanticMemory()

    async def handle_prompt(self, prompt: str):
        # Add prompt to short-term memory
        self.short_memory.add("user", prompt)

        # Optionally check semantic memory
        relevant_docs = self.semantic_memory.query(prompt)
        context = "\n".join(d["text"] for d in relevant_docs)

        # Call LLM with memory context
        response = ollama.chat(
            model="llama3.2:3b",
            messages=[
                {"role": "system", "content": "Use previous context and facts."},
                {"role": "user", "content": f"{prompt}\nContext:\n{context}"}
            ]
        )

        # Store LLM output in memory
        self.short_memory.add("assistant", response["message"]["content"])
        self.semantic_memory.add(response["message"]["content"])

        return response["message"]["content"]

# Run example
agent = AgentWithMemory()
asyncio.run(agent.handle_prompt("What is the company policy on remote work?"))
