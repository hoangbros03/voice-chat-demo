from __future__ import annotations

from queue import Queue

import numpy as np
from fastrtc import StreamHandler


class EchoHandler(StreamHandler):
    def __init__(self):
        super().__init__()
        self.queue = Queue()

    def receive(self, frame: tuple[int, np.ndarray]) -> None:
        self.queue.put(frame)

    def emit(self) -> None:
        return self.queue.get()

    def copy(self) -> StreamHandler:
        return EchoHandler()

    def shutdown(self) -> None:
        pass

    def start_up(self) -> None:
        pass
