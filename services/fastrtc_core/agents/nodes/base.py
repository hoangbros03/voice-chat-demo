from __future__ import annotations

import abc
from typing import Any

from agents.state import State
from pydantic import BaseModel


class BaseNode(BaseModel):

    class Config:
        arbitrary_types_allowed = True

    @abc.abstractmethod
    def execute(self, state: State) -> Any:
        pass


class AsyncBaseNode(BaseModel):

    class Config:
        arbitrary_types_allowed = True

    @abc.abstractmethod
    async def __call__(self, state: State) -> Any:
        pass
