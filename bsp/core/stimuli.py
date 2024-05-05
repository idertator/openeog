from numpy import int32, linspace, ndarray, pi, sin, zeros
from numpy.random import randint


def saccadic_stimuli(
    length: int,
    saccades: int,
    variability: float = 0.05,
) -> ndarray:
    """Generate a saccadic stimulus

    Args:
        length (int): Length of the stimulus
        saccades (int): Number of saccades
        variability (float, optional): Variability of the saccades. Defaults to 0.05.

    Returns:
        ndarray: Saccadic stimulus
    """
    fixations_count = saccades + 3
    center = length / fixations_count
    delta = int(center * variability)
    low, high = center - delta, center + delta

    fixations = randint(low, high, size=fixations_count, dtype=int32)
    edges_samples = fixations[0] + fixations[-1] + (length - sum(fixations))

    fixations[0] = edges_samples // 2
    fixations[-1] = edges_samples // 2 + edges_samples % 2

    assert sum(fixations) == length

    result = zeros(length, dtype=int32)

    start = int(fixations[0])
    for idx in range(1, len(fixations) - 1):
        end = start + int(fixations[idx])
        if idx % 2 == 0:
            result[start:end] = -1
        else:
            result[start:end] = 1

        start = end

    return result


def pursuit_stimuli(
    length: int,
    speed: float = 1.5,
) -> ndarray:
    """Generate a pursuit stimulus

    Args:
        length (int): Length of the stimulus
        speed (float, optional): Speed of the stimulus in °/s. Defaults to 2.0.
        angle (int, optional): Angle of the stimulus. Defaults to 60.

    Returns:
        ndarray: Pursuit stimulus
    """
    num_cycles = (speed * 1000) / 360
    x = linspace(0, num_cycles * 2 * pi, length)

    return sin(x)
