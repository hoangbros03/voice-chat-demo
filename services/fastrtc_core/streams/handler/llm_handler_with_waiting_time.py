from __future__ import annotations

import asyncio
import logging
from typing import Any

import numpy as np
from streams.handler.utils import load_keyboard_sound
from streams.handler.utils import stream_keyboard_sound

KEYBOARD_AUDIO_PATH = 'resources/sounds/keyboard.mp3'
WAITING_MESSAGE = 'Let me think for a moment...'
logging.basicConfig(level=logging.INFO)

sound_chunks = load_keyboard_sound(KEYBOARD_AUDIO_PATH)


async def llm_handler_with_waiting_time(
    audio: tuple[int, np.ndarray],
    stt_model: Any,
    tts_model: Any,
    agent_graph: Any,
    thread_id: str,  # For multi-turn conversation tracking
):
    # Step 1: Speech-to-Text
    transcription = stt_model.stt(audio)
    logging.info(f"Transcription: {transcription}")

    # Step 2: Process with Agent Graph multi-turn
    initial_state = {
        'messages': [{'role': 'user', 'content': transcription}],
    }

    # Configure with thread_id for conversation persistence
    config = {'configurable': {'thread_id': thread_id}}

    # Invoke graph - it will automatically load history from checkpointer
    llm_task = asyncio.create_task(
        agent_graph.ainvoke(initial_state, config),
    )
    while not llm_task.done():
        async for audio_chunk in tts_model.stream_tts(WAITING_MESSAGE):
            yield audio_chunk

        # While waiting for LLM response, stream keyboard sound
        async for audio_chunk in stream_keyboard_sound(
            sound_chunks,
            max_duration_s=5,
        ):
            yield audio_chunk

        break

    # Extract assistant's response (last message)
    result = await llm_task
    response = result['messages'][-1]['content']

    # Step 3: Text-to-Speech
    async for audio_chunk in tts_model.stream_tts(response):
        yield audio_chunk
