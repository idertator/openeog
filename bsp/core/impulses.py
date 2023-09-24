from typing import Iterator

from numpy import ndarray
from scipy.signal import medfilt
from sklearn.cluster import KMeans

from .denoising import denoise
from .differentiation import differentiate


def impulses(channel: ndarray) -> Iterator[tuple[int, int]]:
    """Iterate over the impulses present in the channel

    Args:
        channel (ndarray): Channel

    Yields:
        tuple[int, int]: (start, end) of the impulse
    """
    denoised_channel = denoise(channel)
    derived_channel = abs(medfilt(differentiate(denoised_channel), 11))

    X = derived_channel.reshape((len(derived_channel), -1))
    labels = KMeans(n_clusters=2, n_init="auto").fit_predict(X)

    def iterate_clusters():
        start = None
        for idx, label in enumerate(labels):
            if label == 1:
                if start is None:
                    start = idx
            else:
                if start is not None:
                    yield start, idx
                start = None

    samples = len(channel)
    for start, end in iterate_clusters():
        while start > 0 and derived_channel[start] > derived_channel[start - 1]:
            start -= 1

        while end < samples - 1 and derived_channel[end] > derived_channel[end + 1]:
            end += 1

        yield start, end
