import asyncio
from crawl4ai import *

async def main():
    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(
            url="https://www.espn.com.au/nba/game/_/gameId/401810614/pacers-raptors",
        )
        print(result.markdown)
    result

if __name__ == "__main__":
    asyncio.run(main())