from typing import Iterator

from numpy import ndarray

from .denoising import denoise_35
from .differentiation import differentiate


def saccades(
    channel: ndarray,
    angle: int,
    tolerance: float = 0.2,
) -> Iterator[tuple[int, int]]:
    """Saccade identification with automatic velocity threshold

    Args:
        channel (ndarray): channel
        angle (int): stimulation angle
        tolerance (float, optional): Amplitude tolerance of stimuli. Defaults to 0.2.

    Yields:
        Iterator[tuple[int, int]]: Saccades onset and offset
    """
    velocities = differentiate(denoise_35(channel))
    threshold = velocities.std()
    velocities = abs(velocities)
    right = len(channel) - 1

    delta_amplitude = angle * tolerance
    min_amplitude, max_amplitude = angle - delta_amplitude, angle + delta_amplitude

    idx = 0
    onset = None
    offset = None
    while idx <= right:
        if velocities[idx] > threshold:
            if onset is None:
                onset = idx
            offset = idx
        elif onset is not None:
            while onset > 0 and velocities[onset] > velocities[onset - 1]:
                onset -= 1

            while offset < right and velocities[offset] > velocities[offset + 1]:
                offset += 1

            window = channel[onset : offset + 1]
            amplitude = window.max() - window.min()

            if min_amplitude <= amplitude <= max_amplitude:
                yield onset, offset

            onset = None
            offset = None

        idx += 1
