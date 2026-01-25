from __future__ import annotations
from settings import Settings
from fastmcp import Client

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
        self.client = Client(settings.mcp.server_url)
