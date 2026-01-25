from __future__ import annotations

from agents.nodes.base import BaseNode
from agents.prompts.answering import ANSWERING_SYSTEM_PROMPT
from agents.state import State


class StateInitNode(BaseNode):
    async def __call__(self, state: State) -> dict:
        """Standard LangGraph node signature - takes only state."""
        return self.execute(state)

    def execute(self, state: State) -> dict:
        # Initialize state with system prompt if not present
        if not state.messages or state.messages[0].get('role') != 'system':
            full_messages = [{
                'role': 'system',
                'content': ANSWERING_SYSTEM_PROMPT,
            }] + state.messages
        else:
            full_messages = state.messages
        return {'messages': full_messages}
