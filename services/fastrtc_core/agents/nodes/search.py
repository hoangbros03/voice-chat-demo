from __future__ import annotations

from agents.nodes.base import AsyncBaseNode
from agents.state import State
from clients.mcp_client import MCPClient

mcp_client = MCPClient().client


class SearchNode(AsyncBaseNode):
    async def __call__(self, state: State) -> dict:
        """Standard LangGraph node signature - takes only state."""
        return self.execute(state)

    async def execute(self, state: State) -> dict:
        # Initialize state with empty messages list
        search_results = await self.search_tool(state.search_query)
        return {'search_results': search_results}

    async def search_tool(query: str) -> dict:
        # Initialize MCP client connected to your server
        result = await mcp_client.call_tool('search', {'query': query})
        return result  # e.g., {"results": ["url1", "url2"]}
