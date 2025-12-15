import asyncio
from coordinator_agent import CoordinatorAgent
from critic_agent import CriticAgent

async def main():
    coordinator = CoordinatorAgent()
    critic = CriticAgent()

    # Step 1: Get expert agent outputs
    expert_results = await coordinator.handle_prompt_split(
        "What is the weather in Sydney and company policy on remote work?"
    )
    # example: [{"agent": "WeatherAgent", "answer": "It will rain"}, ...]

    # Step 2: Verify & critique
    critique_result = await critic.verify(expert_results)

    # Step 3: Pass to summary agent (optional)
    print("Verified outputs:", critique_result["verified_answers"])
    print("Issues found:", critique_result["issues"])
    print("Confidence:", critique_result["overall_confidence"])

asyncio.run(main())
