from __future__ import annotations

from mcp import Client
from settings import Settings

settings = Settings()


class MCPClient:
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super().__new__(cls)
        return cls.instance

    def __init__(self):
        if hasattr(self, '_initialized'):
            return
        self._initialized = True
        self.client = Client(server_url=settings.mcp.server_url)
