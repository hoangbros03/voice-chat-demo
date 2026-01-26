from __future__ import annotations

from typing import Any

import numpy as np
from fastrtc import get_stt_model
from fastrtc import get_tts_model
from fastrtc import ReplyOnPause
from fastrtc import Stream
from fastrtc import AlgoOptions
from streams.handler import HANDLER_FUNCTIONS
from streams.handler import HandlerType

SPEECH_THRESHOLD = 0.3  # Higher = less sensitive to background noise


class ReplyOnPauseStream(Stream):
    def __init__(
        self, handler_name: str = 'simple_llm', agent_graph: Any = None,
    ) -> None:
        self.stt_model = get_stt_model()
        self.tts_model = get_tts_model()
        if agent_graph is None:
            raise ValueError(
                'agent_graph must be provided for ReplyOnPauseStream',
            )
        self.agent_graph = agent_graph
        self.thread_id = (
            'default_thread'  # For multi-turn conversation tracking
        )

        self.handler_func = HANDLER_FUNCTIONS.get(
            HandlerType(handler_name), None,
        )
        assert self.handler_func is not None, (
            f'Handler function for {handler_name} not found.'
        )

        vad_options = AlgoOptions(
            speech_threshold=SPEECH_THRESHOLD,
        )

        super().__init__(
            handler=ReplyOnPause(self.handler, algo_options=vad_options),
            modality='audio',
            mode='send-receive',
        )

    async def echo(self, audio: tuple[int, np.ndarray]):
        transcription = self.stt_model.stt(audio)
        async for audio_chunk in self.tts_model.stream_tts(transcription):
            yield audio_chunk

    async def handler(
        self,
        audio: tuple[int, np.ndarray],
    ):
        assert self.handler_func is not None  # for mypy
        async for audio_chunk in self.handler_func(
            audio,
            self.stt_model,
            self.tts_model,
            self.agent_graph,
            self.thread_id,
        ):
            yield audio_chunk
