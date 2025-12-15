from ollama import chat
from multi_agent.agents.base_agent import BaseAgent

from llama_index.tools.mcp import BasicMCPClient

class WeatherAgent(BaseAgent):
    def __init__(self):
        super().__init__("WeatherAgent")

    @staticmethod
    async def fetch_weather() -> str:
        mcp_client = BasicMCPClient("http://127.0.0.1:8000/sse")

        result = await mcp_client.call_tool("get_sydney_weather")
        return result
    
    async def handle_task(self, task):
        weather = await self.fetch_weather()
        weather_html = weather.content[0].text

        response = chat(
            model='llama3.2:3b',
            messages=[
                {"role": "system", "content": "You are an agent expert for reading JSON and getting weather data. Provide an the weather data from the JSON."},
                {"role": "user", "content": f"Answer the prompt\n{task}\nwith weather data from the JSON,:\n{weather_html}"}
            ]
        )


        resp = response['message']['content']
        return resp