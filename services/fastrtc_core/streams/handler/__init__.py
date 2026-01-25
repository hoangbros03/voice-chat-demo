from __future__ import annotations

from enum import Enum

from streams.handler.async_echo_handler import AsyncEchoHandler
from streams.handler.echo_handler import EchoHandler
from streams.handler.llm_handler_with_waiting_time import (
    llm_handler_with_waiting_time,
)
from streams.handler.simple_llm_handler import simple_llm_handler
from streams.handler.simple_webcam_handler import flip_vertically_handler

__all__ = [
    'AsyncEchoHandler',
    'EchoHandler',
    'flip_vertically_handler',
    'llm_handler_with_waiting_time',
    'simple_llm_handler',
]


class HandlerType(str, Enum):
    ECHO = 'echo'
    SIMPLE_LLM = 'simple_llm'
    LLM_WITH_WAITING_TIME = 'llm_with_waiting_time'


HANDLER_FUNCTIONS = {
    HandlerType.SIMPLE_LLM: simple_llm_handler,
    HandlerType.LLM_WITH_WAITING_TIME: llm_handler_with_waiting_time,
}
