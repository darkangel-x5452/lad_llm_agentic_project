from multi_agent.agents.orchestrator.orchestrator import OrchestratorAgent
import asyncio

async def main():
    orchestrator = OrchestratorAgent()

    prompts = [
        # "Summarize this paragraph about AI.",
        # "Write a Python function to calculate factorial.",
        "Write a Python function code to calculate factorial and also explain what factorial is.",
        # "What is the weather in Sydney tomorrow?",
        # "Calculate the sum of 123 + 456.",
        # "Write a summary and also generate code to parse text."
    ]

    for prompt in prompts:
        print(f"\nPrompt: {prompt}")
        summary = await orchestrator.handle_prompt(prompt)
        print(f"COORDINATOR SUMMARY")
        print(f"{summary}")

if __name__ == "__main__":
    print("hi")
    # main()
    asyncio.run(main())
    # print(asyncio.run(weather_agent("What's the weather in Sydney today?")))
    print("bye")
