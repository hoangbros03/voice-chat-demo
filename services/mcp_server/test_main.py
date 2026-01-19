from __future__ import annotations

import asyncio
import json

from fastmcp import Client


async def main():
    # FastMCP Client automatically manages the connection and infers
    # the transport (Stdio) from the file extension (.py).
    # server = FastMCP("web-tools")
    client = Client('http://127.0.0.1:8000/mcp')
    async with client:
        tools = await client.list_tools()
        print('Available tools:', tools)
        # 1. Search: Call the tool and parse the JSON result
        search_result = await client.call_tool(
            'web_search',
            {'query': 'MCP protocol', 'k': 2},
        )

        # FastMCP returns raw MCP content (usually JSON text for complex data),
        # so we parse it to get the list of results.
        results = json.loads(search_result.content[0].text)
        url = results[0]['url']

        # 2. Crawl: Call the tool with the extracted URL
        crawl_result = await client.call_tool(
            'web_crawl',
            {'url': url},
        )

        # Extract and print the text content
        content = crawl_result.content[0].text
        print(content[:1000])

asyncio.run(main())
