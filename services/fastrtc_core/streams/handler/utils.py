from __future__ import annotations

import asyncio

import numpy as np
from pydub import AudioSegment


def echo_same(audio: tuple[int, np.ndarray]):
    """Returns the same audio frame that was received."""
    yield audio


def load_keyboard_sound(
    path: str, target_rate: int = 16000, chunk_ms: int = 100,
):
    """Load and process keyboard sound into audio chunks.

    Args:
        path: Path to the audio file to load
        target_rate: Target sample rate in Hz (default: 16000)
        chunk_ms: Duration of each chunk in milliseconds (default: 100)

    Returns:
        List of audio chunks as tuples of (sample_rate, audio_data)
    """
    audio = (
        AudioSegment.from_file(path)
        .set_frame_rate(target_rate)  # 16k
        .set_channels(1)  # Mono
    )

    # Convert PCM int16 (-32768 to 32767) -> float32 (-1.0 to 1.0)
    samples = (
        np.array(audio.get_array_of_samples()).astype(np.float32) / 32768.0
    )

    samples_per_chunk = int(target_rate * chunk_ms / 1000)
    chunks = []

    for i in range(0, len(samples), samples_per_chunk):
        chunk = samples[i: i + samples_per_chunk]
        if len(chunk) == 0:
            continue
        chunks.append((target_rate, chunk))
    return chunks


async def stream_keyboard_sound(
    chunks: list[tuple[int, np.ndarray]], max_duration_s: int = 5,
):
    """Asynchronously stream keyboard sound chunks.

    Args:
        max_duration_s: Maximum duration to stream in seconds (default: 5)

    Yields:
        Audio chunks as tuples of (sample_rate, audio_data)
    """
    if max_duration_s <= 0:
        return

    total_samples = 0
    total_samples_allowed = None

    for sample_rate, chunk in chunks:
        # Initialize allowed sample budget once we know the sample rate
        if total_samples_allowed is None:
            total_samples_allowed = int(max_duration_s * sample_rate)

        if total_samples >= total_samples_allowed:
            break

        remaining_samples = total_samples_allowed - total_samples

        # Trim the chunk if it would exceed the allowed duration
        if len(chunk) > remaining_samples:
            chunk = chunk[:remaining_samples]

        if len(chunk) == 0:
            break

        yield (sample_rate, chunk)
        total_samples += len(chunk)

        await asyncio.sleep(0)  # allow event loop to breathe
