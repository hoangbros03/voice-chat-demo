from __future__ import annotations

import asyncio

import numpy as np
from fastrtc import AsyncStreamHandler
from fastrtc import wait_for_item


class AsyncEchoHandler(AsyncStreamHandler):
    """Simple Async Echo Handler"""

    def __init__(self) -> None:
        super().__init__(input_sample_rate=24000)
        self.queue: asyncio.Queue = asyncio.Queue()

    async def receive(self, frame: tuple[int, np.ndarray]) -> None:
        await self.queue.put(frame)

    async def emit(self) -> None:
        return await wait_for_item(self.queue)

    def copy(self):
        return AsyncEchoHandler()

    async def shutdown(self):
        pass

    async def start_up(self) -> None:
        pass
