import numpy as np


def scale_channel(value: np.ndarray, angle: float) -> np.ndarray:
    """Scale the channel to the angle

    Args:
        value (ndarray): Channel
        angle (float): Angle

    Returns:
        ndarray: Channel
    """
    # Llevar el estímulo al angulo indicado
    min_value = min(value)
    max_value = max(value)

    amplitude_raw = max_value - min_value
    scale = angle / amplitude_raw
    return value * scale


def center_signal(value: np.ndarray) -> np.ndarray:
    """Center the signal

    Args:
        value (ndarray): Channel

    Returns:
        ndarray: Channel
    """
    # Centrar la señal
    return value - value.mean()


def mse(s1: np.ndarray, s2: np.ndarray) -> float:
    """Mean squared error

    Args:
        s1 (ndarray): Channel
        s2 (ndarray): Channel

    Returns:
        float: MSE
    """
    return np.sum((s1 - s2) ** 2) / len(s1)


def move(s: np.ndarray, count: int = 1) -> np.ndarray:
    """Move the signal

    Args:
        s (ndarray): Channel
        count (int, optional): Count. Defaults to 1.

    Returns:
        ndarray: Channel
    """
    return np.hstack((np.ones(count) * s[0], s[:-count]))
