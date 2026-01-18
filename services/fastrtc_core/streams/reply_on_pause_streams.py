from __future__ import annotations

from typing import Any

import numpy as np
from fastrtc import get_stt_model
from fastrtc import get_tts_model
from fastrtc import ReplyOnPause
from fastrtc import Stream
from streams.handler.simple_llm_handler import simple_llm_handler


class ReplyOnPauseStream(Stream):
    def __init__(
        self, handler_name: str = 'default', agent_graph: Any = None,
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
        if handler_name == 'simple_llm':
            handler = ReplyOnPause(self.simple_llm_handler)
        else:
            handler = ReplyOnPause(self.echo)

        super().__init__(
            handler=handler,
            modality='audio',
            mode='send-receive',
        )

    async def echo(self, audio: tuple[int, np.ndarray]):
        transcription = self.stt_model.stt(audio)
        async for audio_chunk in self.tts_model.stream_tts(transcription):
            yield audio_chunk

    async def simple_llm_handler(
        self,
        audio: tuple[int, np.ndarray],
    ):
        async for audio_chunk in simple_llm_handler(
            audio,
            self.stt_model,
            self.tts_model,
            self.agent_graph,
            self.thread_id,
        ):
            yield audio_chunk
