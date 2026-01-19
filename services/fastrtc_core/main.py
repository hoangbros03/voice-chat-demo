from __future__ import annotations

from agents.graph_builder import get_compiled_graph
from streams import ReplyOnPauseStream as Stream

graph = get_compiled_graph()

stream = Stream(
    handler_name='llm_with_waiting_time',
    agent_graph=graph,
)

if __name__ == '__main__':
    stream.ui.launch()
