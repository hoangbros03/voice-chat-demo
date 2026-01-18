from __future__ import annotations

import numpy as np


def flip_vertically_handler(image):
    return np.flip(image, axis=0)
