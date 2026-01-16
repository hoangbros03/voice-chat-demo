from fastrtc import Stream
import numpy as np


def flip_vertically(image):
    return np.flip(image, axis=0)

stream = Stream(
    handler=flip_vertically,
    modality="video",
    mode="send-receive",
)

if __name__ == "__main__":
    stream.ui.launch()