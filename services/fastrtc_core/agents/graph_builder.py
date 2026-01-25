from __future__ import annotations

from agents.nodes.answering import AnsweringNode
from agents.nodes.plan import PlanNode
from agents.nodes.state_init import StateInitNode
from agents.nodes.search import SearchNode
from agents.state import State
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END
from langgraph.graph import START
from langgraph.graph import StateGraph

nodes = {
    'init': StateInitNode(),
    'plan': PlanNode(),
    'answering': AnsweringNode(),
    'search': SearchNode(),
}


def get_graph_builder() -> StateGraph[State]:
    graph_builder = StateGraph(State)
    graph_builder.add_node('init', nodes['init']),
    graph_builder.add_node('plan', nodes['plan']),
    graph_builder.add_node('answering', nodes['answering'])
    graph_builder.add_node('search', nodes['search'])
    graph_builder.add_edge(START, 'init')
    graph_builder.add_edge('init', 'plan')
    graph_builder.add_conditional_edges(
        'plan',
        # Placeholder for search
        lambda state: 'answering' if not state.needs_search else 'search',
    )
    graph_builder.add_edge('search', 'answering')
    graph_builder.add_edge('answering', END)
    return graph_builder


def get_compiled_graph():
    """Get compiled graph with checkpointer for multi-turn conversations."""
    graph_builder = get_graph_builder()
    memory = MemorySaver()  # In-memory checkpointer for conversation history
    return graph_builder.compile(checkpointer=memory)
