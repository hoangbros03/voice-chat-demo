from __future__ import annotations

import logging
import sys
sys.path.append('../settings')

import requests
from crawl4ai import AsyncWebCrawler
from fastmcp import FastMCP
from settings import Settings

logging.basicConfig(level=logging.INFO)
settings = Settings()
mcp = FastMCP('web-tools')


@mcp.tool(name='web_search', description='Search the web for information.')
def web_search(query: str, k: int = 5) -> list[dict]:
    """Search the web and return top results"""
    resp = requests.post(
        'https://api.tavily.com/search',
        json={
            'query': query,
            'max_results': k,
        },
        headers={
            'Accept': 'application/json',
            'Authorization': 'Bearer ' + settings.search.key,
        },
    )
    data = resp.json()
    return [
        {'title': r['title'], 'url': r['url'], 'content': r['content']}
        for r in data['results']
    ]


@mcp.tool(name='web_crawl', description='Get the content of a web page.')
async def web_crawl(url: str):
    async with AsyncWebCrawler() as crawler:
        page = await crawler.arun(url)
        try:
            return page.markdown  # ignore: noqa
        except Exception:
            logging.error(f"Failed to extract content from {url}")
            return ''
