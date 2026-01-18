from __future__ import annotations

import logging
from typing import Any

import numpy as np

logging.basicConfig(level=logging.INFO)


async def simple_llm_handler(
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
    result = agent_graph.invoke(initial_state, config)

    # Extract assistant's response (last message)
    response = result['messages'][-1]['content']

    # Step 3: Text-to-Speech
    async for audio_chunk in tts_model.stream_tts(response):
        yield audio_chunk
