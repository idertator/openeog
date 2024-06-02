import numpy as np
from scipy import signal
from scipy.signal import coherence, medfilt

from bsp.core import differentiate, helpers
from bsp.core.denoising import denoise_35
from bsp.core.models import Test
from bsp.core.saccades import saccades


class PursuitBiomarkers:
    def __init__(
        self,
        test: Test,
        to_cut: int,
        invert_signal: bool = False,
        **kwargs,
    ):
        """Constructor

        Args:
            test (Test): test
            to_cut (int): number of samples to cut
            invert_signal (bool, optional): invert signal. Defaults to False.

        Returns:
            PursuitBiomarkers: object
        """
        self.angle = test.angle
        self.horizontal_channel = None
        self.horizontal_cutted = None

        if invert_signal:
            self.horizontal_channel = test.hor_channel.copy()[to_cut:-to_cut] * -1
            self.horizontal_cutted = test.hor_channel_raw.copy()[to_cut:-to_cut] * -1
        else:
            self.horizontal_channel = test.hor_channel.copy()[to_cut:-to_cut]
            self.horizontal_cutted = test.hor_channel_raw.copy()[to_cut:-to_cut]
        amplitude = self.horizontal_channel.max() - self.horizontal_channel.min()

        self.stimuli_channel = test.hor_stimuli.copy()[to_cut:-to_cut]
        self.stimuli_channel -= self.stimuli_channel.mean()
        self.stimuli_channel *= amplitude * 2
        self.stimuli_cutted = test.hor_stimuli_raw.copy()[to_cut:-to_cut]

    @property
    def waveform_mse(self) -> tuple[int, float]:
        """Waveform MSE

        Returns:
            tuple[int, float]: displacement, error
        """
        count = 2000
        errors = np.zeros(count)
        for i in range(1, count + 1):
            offset = helpers.move(self.horizontal_channel, i)
            errors[i - 1] = helpers.mse(self.stimuli_channel, offset)
            best_displacement = errors.argmin()
            best_error = errors[best_displacement]

        return best_displacement, best_error

    @property
    def latency_mean(self) -> float:
        """Latency Mean

        Returns:
            float: latency (in seconds)
        """
        centered_channel = helpers.center_signal(self.horizontal_cutted)
        centered_stimuli = helpers.center_signal(self.stimuli_cutted)
        scaled_channel = helpers.scale_channel(centered_channel, self.angle)
        scaled_stim_channel = helpers.scale_channel(centered_stimuli, self.angle)

        denoised_channel = denoise_35(scaled_channel)

        peaks_channel = signal.find_peaks_cwt(abs(denoised_channel), 1000)[:-1]
        peaks_stim_channel = signal.find_peaks_cwt(abs(scaled_stim_channel), 1000)[:-1]

        displacements = peaks_stim_channel - peaks_channel

        latency_res = int(round(displacements.mean(), 0))

        return latency_res / 1000.0

    @property
    def corrective_saccades_count(self) -> int:
        """Corrective saccades count

        Returns:
            int: number of saccades
        """
        num_sacc = 0
        for index in range(self.angle + 1):
            for start, end in saccades(self.horizontal_channel, index):
                num_sacc += 1
        return num_sacc

    @property
    def velocity_mean(self) -> float:
        """Velocity Mean

        Returns:
            float: velocity (in degrees per second)
        """
        ch_filtered = medfilt(self.horizontal_channel, 201)
        ch_f_vel = differentiate(ch_filtered)
        mean_pursuit = abs(ch_f_vel.mean())
        return mean_pursuit

    @property
    def velocity_gain(self) -> float:
        """Velocity Gain

        Returns:
            float: velocity gain
        """
        mean_ch = self.velocity_mean
        stimuli_vel = differentiate(self.stimuli_channel)
        mean_stimuli = abs(stimuli_vel.mean())
        gain_vel = mean_ch / mean_stimuli

        return gain_vel

    @property
    def spectral_coherence(self) -> float:
        """Spectral Coherence

        Returns:
            float: spectral coherence
        """
        freqs, c = coherence(self.stimuli_channel, self.horizontal_channel, fs=1000.0)
        coherence_factor = (1 - c)[:10].mean()

        return coherence_factor

    @property
    def to_dict(self) -> dict[str, int | float]:
        """To Dict

        Returns:
            dict[str, int | float]: dictionary
        """
        return {
            "waveform_mse": self.waveform_mse,
            "latency_mean": self.latency_mean,
            "corrective_saccades_count": self.corrective_saccades_count,
            "velocity_mean": self.velocity_mean,
            "velocity_gain": self.velocity_gain,
            "spectral_coherence": self.spectral_coherence,
        }
