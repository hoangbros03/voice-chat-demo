from __future__ import annotations

from agents.nodes.base import BaseNode
from agents.state import State
from agents.prompts.answering import ANSWERING_USER_PROMPT
from clients.openai_client.client import OpenAIClient


class AnsweringNode(BaseNode):
    openai_client: OpenAIClient = OpenAIClient()

    def __call__(self, state: State) -> dict:
        """Standard LangGraph node signature - takes only state."""
        return self.execute(state)

    def execute(self, state: State) -> dict:
        # Get all messages from state (includes history)
        latest_user_message = state.messages[-1]['content']

        # Prepare messages for OpenAI
        messages = state.messages[:-1] + [{
            'role': 'user',
            'content': ANSWERING_USER_PROMPT.format(
                user_question=latest_user_message,
                conversation_history=state.messages,
                additional_context=state.search_results,
            ),
        }]

        # Call OpenAI with full conversation history
        response = self.openai_client.completions(messages)

        # Append assistant response
        updated_messages = messages + [{
            'role': 'assistant',
            'content': response,
        }]

        return {'messages': updated_messages}
