from __future__ import annotations

from fastrtc import Stream
from handler import AsyncEchoHandler

stream = Stream(
    handler=AsyncEchoHandler(),
    modality='audio',
    mode='send-receive',
)

if __name__ == '__main__':
    stream.ui.launch()
