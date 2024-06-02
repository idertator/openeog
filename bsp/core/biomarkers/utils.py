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
