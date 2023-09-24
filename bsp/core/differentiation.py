from numpy import array, convolve, ndarray


def differentiate(channel: ndarray) -> ndarray:
    """Super Lanczos 11  numerical differentiation method

    Args:
        channel (ndarray): Channel

    Returns:
        ndarray: Channel
    """
    window = array([300, -294, -532, -503, -296, 0, 296, 503, 532, 294, -300])
    result = convolve(channel, window, "same") / 5148.0
    result[:5] = 0
    result[-5:] = 0
    return result * 1000.0
