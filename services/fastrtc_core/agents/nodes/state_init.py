from __future__ import annotations

from agents.nodes.base import BaseNode
from agents.prompts.answering import ANSWERING_SYSTEM_PROMPT
from agents.state import State


class StateInitNode(BaseNode):
    async def __call__(self, state: State) -> dict:
        """Standard LangGraph node signature - takes only state."""
        return self.execute(state)

    def execute(self, state: State) -> dict:
        # Initialize state with empty messages list
        full_messages = [{
            'role': 'system',
            'content': ANSWERING_SYSTEM_PROMPT,
        }]
        return {'messages': full_messages}
