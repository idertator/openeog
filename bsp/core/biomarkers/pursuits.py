from bsp.core.models import Test
import numpy as np
from scipy import signal
from scipy.fft import fft, fftfreq
from scipy.signal import coherence
from scipy.signal import medfilt
from bsp.core.saccades import saccades
from bsp.core import differentiate

# from functools import cached_property
#
# from numpy import ndarray

#Auxiliar functions
def mse(s1: np.ndarray, s2: np.ndarray) -> float:
    return np.sum((s1 - s2) ** 2) / len(s1)

def move(s: np.ndarray, count: int=1) -> np.ndarray:
    return np.hstack((np.ones(count) * s[0], s[:-count]))

def best_fit(s1: np.ndarray, s2: np.ndarray) -> tuple[int, float]:
    count = 2000
    errors = np.zeros(count)
    best_displacement = 0
    for i in range(1, count + 1):
        offset = move(s2, i)
        errors[i - 1] = mse(s1, offset)
        best_displacement = errors.argmin()
        best_error = errors[best_displacement]
    return best_displacement, best_error

def center_signal(value: np.ndarray) -> np.ndarray:
    return value - value.mean()

def scale_channel(value: np.ndarray, angle: float) -> np.ndarray:
    # Llevar el estímulo al angulo indicado
    min_value = min(value)
    max_value = max(value)

    amplitude_raw = max_value - min_value
    scale = angle / amplitude_raw

    return value * scale

def denoise_35(value: np.ndarray) -> np.ndarray:
    b, a = signal.butter(3, 0.035)
    y = signal.filtfilt(b, a, value)
    return y

# Biomarcador 1
def pursuit_position_mse_biomarker(channel: np.ndarray, stimuli: np.ndarray) -> tuple[int, float]:
    displacement, error = best_fit(stimuli, channel)
    return displacement, error

#Biomarcador 2
def pursuit_latency_biomarker(channel: np.ndarray, stimuli: np.ndarray, angle: int) -> float:
    centered_channel = center_signal(channel)
    scaled_channel = scale_channel(centered_channel, angle)  # pursuit.angle)
    scaled_stim_channel = scale_channel(stimuli, angle)  # pursuit.angle)

    denoised_channel = denoise_35(scaled_channel)

    peaks_channel = signal.find_peaks_cwt(abs(denoised_channel), 1000)[:-1]
    peaks_stim_channel = signal.find_peaks_cwt(abs(scaled_stim_channel), 1000)[:-1]

    displacements = peaks_stim_channel - peaks_channel

    latency_res = int(round(displacements.mean(), 0))

    return latency_res / 1000.0

#Biomarcador 3
def pursuit_saccades_count_biomarker(channel: np.ndarray, angle: int) -> int:
    numSacc = 0
    for index in range (angle):
        for start, end in saccades(channel, index):
            numSacc +=1
    return numSacc

#Biomarcador 4
def pursuit_mean_velocity_biomarker(channel: np.ndarray) -> float:
    ch_filtered = medfilt(channel, 201)
    ch_f_vel = differentiate(ch_filtered)
    mean_pursuit = abs(ch_f_vel.mean())
    return mean_pursuit

#Biomarcador 5
def pursuit_mean_velocity_gain_biomarker(channel: np.ndarray, stimuli: np.ndarray) -> float:
    mean_ch = pursuit_mean_velocity_biomarker(channel)
    stimuli_vel = differentiate(stimuli)
    mean_stimuli = abs(stimuli_vel.mean())
    gain_vel = mean_ch/mean_stimuli
    return gain_vel

#Biomarcador 6
def pursuit_spectral_difference_biomarker(channel: np.ndarray, stimuli: np.ndarray) -> float:
    freqs, c = coherence(stimuli, channel, fs=1000.0)
    coherence_factor = ((1-c)[:10].mean())
    return coherence_factor


class PursuitBiomarkers:
    def __init__(
        self,
        test: Test,
        samples_to_cut: int,
        **kwargs,
    ):
        self.test = test
        self.samples_to_cut = samples_to_cut
        self.horizontal_channel = None
        self.stimuli_channel = None
        self._preprocess_signals()

    def _preprocess_signals(self):
        to_cut = self.samples_to_cut
        # -1 por electrodos invertidos, buscar sol fuera de esta seccion
        self.horizontal_channel = self.test.hor_channel_raw.copy()[to_cut:-to_cut] * -1
        amplitude = self.horizontal_channel.max() - self.horizontal_channel.min()

        self.stimuli_channel = self.test.hor_stimuli_raw[to_cut:-to_cut]
        self.stimuli_channel -= self.stimuli_channel.mean()
        self.stimuli_channel *= (amplitude*2)

    # @cached_property
    # def _filetered_velocity(self) -> ndarray:
    #     return filtro(self.test.hor_channel_raw)

    @property
    def waveform_mse(self) -> float:
        return pursuit_position_mse_biomarker(self.horizontal_channel, self.stimuli_channel)[1]

    @property
    def latency_mean(self) -> float:
        # En segundos
        return pursuit_latency_biomarker(self.horizontal_channel, self.stimuli_channel, self.test.angle)

    @property
    def corrective_saccades_count(self) -> int:
        return pursuit_saccades_count_biomarker(self.horizontal_channel, self.test.angle)

    @property
    def velocity_mean(self) -> float:
        return pursuit_mean_velocity_biomarker(self.horizontal_channel)
        # velocities = self._filetered_velocity

    @property
    def velocity_gain(self) -> float:
        return pursuit_mean_velocity_gain_biomarker(self.horizontal_channel, self.stimuli_channel)
        # velocities = self._filetered_velocity

    @property
    def spectral_coherence(self) -> float:
        return pursuit_spectral_difference_biomarker(self.horizontal_channel, self.stimuli_channel)

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
