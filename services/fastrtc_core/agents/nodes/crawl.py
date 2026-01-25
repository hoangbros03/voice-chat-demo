from __future__ import annotations

from agents.nodes.base import AsyncBaseNode
from agents.state import State
from clients.mcp_client import MCPClient

mcp_client = MCPClient().client


class CrawlNode(AsyncBaseNode):
    async def __call__(self, state: State) -> dict:
        """Standard LangGraph node signature - takes only state."""
        return self.execute(state)

    async def execute(self, state: State) -> dict:
        # Initialize state with empty messages list
        crawl_result = await self.crawl_tool(state.crawl_url)
        return {'crawl_results': crawl_result}

    async def crawl_tool(url: str) -> dict:
        # Initialize MCP client connected to your server
        result = await mcp_client.call_tool('crawl', {'url': url})
        return result
