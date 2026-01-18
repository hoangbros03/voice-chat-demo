from __future__ import annotations

import numpy as np


def echo_same(audio: tuple[int, np.ndarray]):
    """Returns the same audio frame that was received."""
    yield audio
