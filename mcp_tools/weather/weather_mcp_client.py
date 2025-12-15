import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


from llama_index.tools.mcp import BasicMCPClient, McpToolSpec
from llama_index.tools.mcp import (
    get_tools_from_mcp_url,
    aget_tools_from_mcp_url,
)

async def get_weather() -> str:
    mcp_client = BasicMCPClient("http://127.0.0.1:8000/sse")

    mcp_tools = McpToolSpec(client=mcp_client) # you can also pass list of allowed tools
    tools = await mcp_tools.to_tool_list_async()

    for tool in tools:
        print(tool.metadata.name, tool.metadata.description)
    # result = await mcp_client.call_tool("add", {"a": 5, "b": 10})
    result = await mcp_client.call_tool("get_sydney_weather")
    return result

if __name__ == "__main__":
    asyncio.run(get_weather())