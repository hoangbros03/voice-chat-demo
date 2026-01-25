from __future__ import annotations

from agents.nodes.answering import AnsweringNode
from agents.nodes.state_init import StateInitNode
from agents.state import State
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END
from langgraph.graph import START
from langgraph.graph import StateGraph

nodes = {
    'init': StateInitNode(),
    'answering': AnsweringNode(),
}


def get_graph_builder() -> StateGraph[State]:
    graph_builder = StateGraph(State)
    graph_builder.add_node('init', nodes['init']),
    graph_builder.add_node('answering', nodes['answering'])
    # graph_builder.set_entry_point('answering')
    # graph_builder.set_finish_point('answering')
    graph_builder.add_edge(START, 'init')
    graph_builder.add_edge('init', 'answering')
    graph_builder.add_edge('answering', END)
    return graph_builder


def get_compiled_graph():
    """Get compiled graph with checkpointer for multi-turn conversations."""
    graph_builder = get_graph_builder()
    memory = MemorySaver()  # In-memory checkpointer for conversation history
    return graph_builder.compile(checkpointer=memory)
