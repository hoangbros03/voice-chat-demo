from __future__ import annotations

from typing import Any

from pydantic import BaseModel


class State(BaseModel):
    messages: list[dict[str, Any]]
    needs_search: bool = False
    search_reason: str = ''
