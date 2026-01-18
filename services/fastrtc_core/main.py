from __future__ import annotations

from agents.graph_builder import get_compiled_graph
from fastrtc import ReplyOnPause
from fastrtc import Stream
from streams.handler import simple_llm_handler

graph = get_compiled_graph()

stream = Stream(
    handler=ReplyOnPause(simple_llm_handler),
    modality='audio',
    mode='send-receive',
)

if __name__ == '__main__':
    stream.ui.launch()
