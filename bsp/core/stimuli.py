import numpy as np

from .models import Direction


def saccadic_stimuli(
    length: int,
    saccades: int,
    variability: float = 0.05,
) -> np.ndarray:
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

    fixations = np.random.randint(low, high, size=fixations_count, dtype=np.int32)
    edges_samples = fixations[0] + fixations[-1] + (length - sum(fixations))

    fixations[0] = edges_samples // 2
    fixations[-1] = edges_samples // 2 + edges_samples % 2

    assert sum(fixations) == length

    result = np.zeros(length, dtype=np.int32)

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
    length: float,
    speed: float = 30.0,
    sampling_rate: float = 1000.0,
) -> np.ndarray:
    """Generate a pursuit stimulus

    Args:
        length (float): Length of the stimulus in seconds.
        speed (float, optional): Speed of the stimulus in °/s. Defaults to 30.0.
        sampling_rate (float, optional): Sampling frequency in Hz. Defaults to 1000.0.

    Returns:
        ndarray: Pursuit stimulus.
    """
    # Calculate the number of samples
    num_samples = int(length * sampling_rate)

    # Calculate the number of cycles
    num_cycles = (speed * length) / 360

    # Generate the x values for the sine wave
    x = np.linspace(0, num_cycles * 2 * np.pi, num_samples)

    # Generate the sine wave with the given amplitude
    y = np.sin(x)

    return y


class SaccadicStimuliTransitions:
    def __init__(self, stimuli: np.ndarray):
        self.transitions = []
        for idx in range(1, len(stimuli)):
            if stimuli[idx - 1] != stimuli[idx]:
                before_value = stimuli[idx - 1]
                after_value = stimuli[idx]

                if before_value < after_value:
                    self.transitions.append((idx, Direction.Left))
                else:
                    self.transitions.append((idx, Direction.Right))

    def __len__(self) -> int:
        return len(self.transitions)

    def __getitem__(self, pos: int) -> tuple[int, int, int, Direction]:
        if self.transitions:
            idx = 0
            change, direction = self.transitions[idx]
            change_before = change
            while pos > change and idx < len(self.transitions) - 1:
                change_before = change
                idx += 1
                change, direction = self.transitions[idx]
            return idx, change, change_before, direction

        return 0, 0, Direction.Same
