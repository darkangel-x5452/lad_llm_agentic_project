import asyncio
from mcp.client.http import http_client
from mcp import ClientSession

class RetrievalAgent:
    def __init__(self, url="http://localhost:4444"):
        self.url = url

    async def retrieve(self, query: str) -> list:
        async with http_client(self.url) as transport:
            session = ClientSession(transport)
            result = await session.call_tool(
                "retrieve_private_docs",
                {"query": query}
            )
            return result.content[0].json
    