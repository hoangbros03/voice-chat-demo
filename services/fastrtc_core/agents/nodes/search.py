from __future__ import annotations

import json

from agents.nodes.base import AsyncBaseNode
from agents.state import State
from clients.mcp_client import MCPClient

mcp_client = MCPClient().client

TOP_K = 3


class SearchNode(AsyncBaseNode):
    async def __call__(self, state: State) -> dict:
        """Standard LangGraph node signature - takes only state."""
        return await self.execute(state)

    async def execute(self, state: State) -> dict:
        # Initialize state with empty messages list
        search_results = await self.search_tool(state.messages[-1]['content'])
        return {'search_results': search_results}

    async def search_tool(self, query: str) -> dict:
        # Initialize MCP client connected to your server
        async with mcp_client:
            result = await mcp_client.call_tool(
                'web_search',
                {'query': query, 'k': TOP_K},
            )
            return {
                'result': [
                    {
                        'title': item['title'],
                        'url': item['url'],
                        'content': item['content'],
                    } for item in json.loads(result.content[0].text)['result']
                ],
            }
