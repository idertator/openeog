from typing import Iterator

from numpy import mean, median, ndarray

from .impulses import impulses


def _amplitudes(channel: ndarray) -> Iterator[int]:
    """Iterate over the amplitudes of the impulses present in the channel

    Args:
        channel (ndarray): Channel

    Yields:
        int: Amplitude
    """
    for start, end in impulses(channel):
        start_value = channel[start]
        end_value = channel[end]
        amplitude = max(start_value, end_value) - min(start_value, end_value)
        yield amplitude


def _valid_amplitudes(channel: ndarray, tolerance: float = 0.2) -> Iterator[int]:
    """Iterate over the valid amplitudes of the impulses present in the channel

    Args:
        channel (ndarray): Channel
        tolerance (float, optional): Tolerance. Defaults to 0.2.

    Yields:
        int: Amplitude
    """
    amplitudes = list(_amplitudes(channel))
    median_amplitude = median(amplitudes)
    delta = median_amplitude * tolerance
    min_value, max_value = median_amplitude - delta, median_amplitude + delta
    for amplitude in amplitudes:
        if min_value <= amplitude <= max_value:
            yield amplitude


def calibration(
    initial: ndarray,
    final: ndarray,
    angle: int = 30,
) -> tuple[float, float]:
    """Calculate the calibration scale and difference between initial and final

    Args:
        initial (ndarray): Initial channel
        final (ndarray): Final channel
        angle (int, optional): Angle of the stimuli. Defaults to 30.

    Returns:
        tuple[float, float]: Scale and difference
    """
    initial_amplitudes = list(_valid_amplitudes(initial))
    final_amplitudes = list(_valid_amplitudes(final))

    initial_mean = mean(initial_amplitudes)
    final_mean = mean(final_amplitudes)

    initial_scale = angle / initial_mean
    final_scale = angle / final_mean

    scale = (initial_scale + final_scale) / 2
    diff = initial_scale / final_scale

    return scale, diff
