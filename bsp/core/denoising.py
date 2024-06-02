import numpy as np
from scipy import signal


def denoise(channel: np.ndarray) -> np.ndarray:
    """Remove high frequency noise from the channel

    Args:
        channel (ndarray): Channel

    Returns:
        ndarray: Channel
    """
    return signal.medfilt(channel, 101)


def denoise_35(channel: np.ndarray) -> np.ndarray:
    """Remove high frequency noise from the channel

    Args:
        channel (ndarray): Channel

    Returns:
        ndarray: Channel
    """
    # Hacemos un filtrado agresivo ya que lo que nos interesa es la forma de onda
    # en general de la señal para identificar el desfase
    b, a = signal.butter(3, 0.035)
    y = signal.filtfilt(b, a, channel)
    return y
