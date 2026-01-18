from __future__ import annotations

from typing import Any

import numpy as np
from fastrtc import get_stt_model
from fastrtc import get_tts_model
from fastrtc import ReplyOnPause
from fastrtc import Stream


class ReplyOnPauseStream(Stream):
    def __init__(self, handler: Any) -> None:
        self.stt_model = get_stt_model()
        self.tts_model = get_tts_model()
        if not handler:
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
