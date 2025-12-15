import argparse
import json

from mcp.server.fastmcp import FastMCP
import requests
from bs4 import BeautifulSoup

mcp = FastMCP("Sydney Weather Server", host="127.0.0.1", port=8000, json_response=True)
# mcp = FastMCP("Sydney Weather Server")


@mcp.tool()
def get_sydney_weather() -> str:
    """
    Scrape current Sydney weather from a public website
    and return a plain-text summary.
    """

    url = "https://api.bom.gov.au/apikey/v1/forecasts/1hourly/658/223?timezone=Australia%2FSydney"
    resp = requests.get(url, timeout=10)
    resp.raise_for_status()
    resp_json = resp.json()
    

    # soup = BeautifulSoup(resp.text, "html.parser")
    # NOTE: selectors may change — this is expected in scraping
    # temp = soup.select_one(".temp").get_text(strip=True)
    # desc = soup.select_one(".summary").get_text(strip=True)

    return f"{json.dumps(resp_json)}"


# Add an addition tool
@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b


# Add a dynamic greeting resource
@mcp.resource("greeting://{name}")
def get_greeting(name: str) -> str:
    """Get a personalized greeting"""
    return f"Hello, {name}!"


# Add a prompt
@mcp.prompt()
def greet_user(name: str, style: str = "friendly") -> str:
    """Generate a greeting prompt"""
    styles = {
        "friendly": "Please write a warm, friendly greeting",
        "formal": "Please write a formal, professional greeting",
        "casual": "Please write a casual, relaxed greeting",
    }

    return f"{styles.get(style, styles['friendly'])} for someone named {name}."


# Run with streamable HTTP transport
if __name__ == "__main__":
    print("🚀Starting server... ")
    # mcp.run()
    # mcp.run(transport="streamable-http")
    # default="streamable-http"
    default="sse"
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--server_type", type=str, default=default, choices=["sse", "stdio", "streamable-http"]
    )

    args = parser.parse_args()
    mcp.run(args.server_type)
