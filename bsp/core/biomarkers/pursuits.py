from bsp.core.models import Test
import numpy as np
from scipy import signal
from scipy.signal import coherence
from scipy.signal import medfilt
from bsp.core.saccades import saccades
from bsp.core import differentiate


# from functools import cached_property

# Auxiliar functions
def mse(s1: np.ndarray, s2: np.ndarray) -> float:
    return np.sum((s1 - s2) ** 2) / len(s1)


def move(s: np.ndarray, count: int = 1) -> np.ndarray:
    return np.hstack((np.ones(count) * s[0], s[:-count]))


def best_fit(s1: np.ndarray, s2: np.ndarray) -> tuple[int, float]:
    # best_fit(stimuli, horizontal)
    count = 2000
    errors = np.zeros(count)
    for i in range(1, count + 1):
        offset = move(s2, i)
        errors[i - 1] = mse(s1, offset)
        best_displacement = errors.argmin()
        best_error = errors[best_displacement]
    return best_displacement, best_error


def center_signal(value: np.ndarray) -> np.ndarray:
    return value - value.mean()


def scale_channel(value: np.ndarray, angle: float) -> np.ndarray:
    min_value = min(value)
    max_value = max(value)

    amplitude_raw = max_value - min_value
    scale = angle / amplitude_raw

    return value * scale


def denoise_35(value: np.ndarray) -> np.ndarray:
    b, a = signal.butter(3, 0.035)
    y = signal.filtfilt(b, a, value)
    return y


class PursuitBiomarkers:
    def __init__(
            self,
            test: Test,
            samples_to_cut: int,
            invert_signal: bool = False,
            **kwargs,
    ):
        self.invert_signal = invert_signal
        self.test = test
        self.samples_to_cut = samples_to_cut
        self.horizontal_channel = None
        self.horizontal_cutted = None
        self.stimuli_channel = None
        self.stimuli_cutted = None
        self._preprocess_signals()

    def _preprocess_signals(self):
        to_cut = self.samples_to_cut
        if self.invert_signal:
            self.horizontal_channel = self.test.hor_channel.copy()[to_cut:-to_cut] * -1
            self.horizontal_cutted = self.test.hor_channel_raw.copy()[to_cut:-to_cut] * -1
        else:
            self.horizontal_channel = self.test.hor_channel.copy()[to_cut:-to_cut]
            self.horizontal_cutted = self.test.hor_channel_raw.copy()[to_cut:-to_cut]
        amplitude = self.horizontal_channel.max() - self.horizontal_channel.min()

        self.stimuli_channel = self.test.hor_stimuli.copy()[to_cut:-to_cut]
        self.stimuli_channel -= self.stimuli_channel.mean()
        self.stimuli_channel *= (amplitude * 2)
        self.stimuli_cutted = self.test.hor_stimuli_raw.copy()[to_cut:-to_cut]

    # @cached_property
    # def _filetered_velocity(self) -> ndarray:
    #     return filtro(self.test.hor_channel_raw)

    @property
    def waveform_mse(self) -> tuple[int, float]:
        return best_fit(self.stimuli_channel, self.horizontal_channel)

    @property
    def latency_mean(self) -> float:
        # En segundos
        centered_channel = center_signal(self.horizontal_cutted)
        centered_stimuli = center_signal(self.stimuli_cutted)
        scaled_channel = scale_channel(centered_channel, self.test.angle)
        scaled_stim_channel = scale_channel(centered_stimuli, self.test.angle)

        denoised_channel = denoise_35(scaled_channel)

        peaks_channel = signal.find_peaks_cwt(abs(denoised_channel), 1000)[:-1]
        peaks_stim_channel = signal.find_peaks_cwt(abs(scaled_stim_channel), 1000)[:-1]

        displacements = peaks_stim_channel - peaks_channel

        latency_res = int(round(displacements.mean(), 0))

        return latency_res / 1000.0

    @property
    def corrective_saccades_count(self) -> int:
        num_sacc = 0
        for index in range(self.test.angle):
            for start, end in saccades(self.horizontal_channel, index):
                num_sacc += 1
        return num_sacc

    @property
    def velocity_mean(self) -> float:
        ch_filtered = medfilt(self.horizontal_channel, 201)
        ch_f_vel = differentiate(ch_filtered)
        mean_pursuit = abs(ch_f_vel.mean())
        return mean_pursuit

    # velocities = self._filetered_velocity

    @property
    def velocity_gain(self) -> float:
        mean_ch = self.velocity_mean
        stimuli_vel = differentiate(self.stimuli_channel)
        mean_stimuli = abs(stimuli_vel.mean())
        gain_vel = mean_ch / mean_stimuli
        return gain_vel
        # velocities = self._filetered_velocity

    @property
    def spectral_coherence(self) -> float:
        freqs, c = coherence(self.stimuli_channel, self.horizontal_channel, fs=1000.0)
        coherence_factor = ((1 - c)[:10].mean())
        return coherence_factor

    @property
    def to_dict(self) -> dict[str, int | float]:
        return {
            "waveform_mse": self.waveform_mse,
            "latency_mean": self.latency_mean,
            "corrective_saccades_count": self.corrective_saccades_count,
            "velocity_mean": self.velocity_mean,
            "velocity_gain": self.velocity_gain,
            "spectral_coherence": self.spectral_coherence,
        }
