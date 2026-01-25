from __future__ import annotations

from agents.nodes.base import BaseNode
from agents.state import State
from clients.openai_client.client import OpenAIClient


class AnsweringNode(BaseNode):
    openai_client: OpenAIClient = OpenAIClient()

    def __call__(self, state: State) -> dict:
        """Standard LangGraph node signature - takes only state."""
        return self.execute(state)

    def execute(self, state: State) -> dict:
        # Get all messages from state (includes history)
        messages = state.messages

        # Call OpenAI with full conversation history
        response = self.openai_client.completions(messages)

        # Append assistant response
        updated_messages = messages + [{
            'role': 'assistant',
            'content': response,
        }]

        return {'messages': updated_messages}
