from __future__ import annotations

import logging
import re

from agents.nodes.base import BaseNode
from agents.state import State

logging.basicConfig(level=logging.INFO)


class PlanNode(BaseNode):
    def __call__(self, state: State) -> dict:
        """Standard LangGraph node signature - takes only state."""
        return self.execute(state)

    def execute(self, state: State) -> dict:
        # Extract the latest user message
        if not state.messages:
            logging.warning(
                'PlanNode: No messages in state, \
                    defaulting to no search needed.',
            )
            return {
                'needs_search': False,
                'search_reason': 'No user message found',
            }

        # Assume the last message is from the user
        latest_message = state.messages[-1]
        if latest_message.get('role') != 'user':
            logging.warning(
                'PlanNode: Latest message is not from user, \
                    defaulting to no search needed.',
            )
            return {
                'needs_search': False,
                'search_reason': 'Latest message not from user',
            }

        content = latest_message.get('content', '').lower()

        # Check for search-related keywords
        search_keywords = r'\b(search|find|look up|research|query|browse)\b'
        if re.search(search_keywords, content, re.IGNORECASE):
            reason = f"Detected search keyword in: '{content[:50]}...'"
            logging.info(f"PlanNode: {reason}")
            return {'needs_search': True, 'search_reason': reason}

        # Additional heuristics: Questions implying external data
        if re.search(
            r'\b(what is|how to|where can i|tell me about)\b.*\?', content,
        ):
            reason = f"Detected question implying external info: \
                '{content[:50]}...'"
            logging.info(f"PlanNode: {reason}")
            return {'needs_search': True, 'search_reason': reason}

        # Default: No search needed
        logging.info('PlanNode: No search needed based on message content.')
        return {
            'needs_search': False,
            'search_reason': 'No indicators for search',
        }
