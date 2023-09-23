from numpy import ndarray
from scipy.signal import medfilt


def denoise(channel: ndarray) -> ndarray:
    """Remove high frequency noise from the channel

    Args:
        channel (ndarray): Channel

    Returns:
        ndarray: Channel
    """
    return medfilt(channel, 101)
