from numpy import int32, ndarray, zeros
from numpy.random import randint


def horizontal_saccadic_stimulus(
    length: int,
    saccades: int,
    variability: float = 0.05,
) -> ndarray:
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
