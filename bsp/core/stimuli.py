from numpy import int32, ndarray, single, zeros
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
    speed: float,
    angle: int,
) -> ndarray:
    """Generate a pursuit stimulus

    Args:
        length (int): Length of the stimulus
        speed (float): Speed of the stimulus in °/s
        angle (int): Angle of the stimulus

    Returns:
        ndarray: Pursuit stimulus
    """
    result = zeros(length, dtype=single)

    idx = 0
    half = angle // 2
    left, right = -half, half
    current = -half
    delta = speed / 1000.0

    while idx < length:
        result[idx] = current
        current = current + delta
        if current < left:
            current = left
            delta *= -1
        elif current > right:
            current = right
            delta *= -1
        idx += 1

    return result / half
