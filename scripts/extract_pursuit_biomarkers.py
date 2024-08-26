#!env python

from pathlib import Path

import tablib
from tqdm import tqdm

from openeog.core.io import load_study, save_study
from openeog.core.models import Study

from functools import cached_property

import numpy as np
from scipy import signal
from scipy.signal import coherence, medfilt

from openeog.core import differentiate, helpers
from openeog.core.denoising import denoise_35
from openeog.core.models import Saccade, Test
from openeog.core.saccades import saccades


def to_match(peaks_channel: np.ndarray, peaks_stim: np.ndarray) -> np.ndarray:
    res = np.zeros(len(peaks_stim))
    for i in range(0, len(peaks_stim)):
        min_difference = abs(peaks_stim[i] - peaks_channel[0])
        close_value = peaks_channel[0]
        for j in range(0, len(peaks_channel)):
            difference = abs(peaks_stim[i] - peaks_channel[j])
            if difference < min_difference:
                close_value = peaks_channel[j]
                min_difference = difference
        res[i] = close_value
    return res


class PursuitBiomarkers:
    def __init__(
            self,
            test: Test,
            to_cut: int = 100,
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
        self.stimuli_channel = None
        # self.horizontal_cutted = None

        if invert_signal:
            self.horizontal_channel = test.hor_channel.copy()[to_cut:-to_cut] * -1
            # self.horizontal_cutted = test.hor_channel_raw.copy()[to_cut:-to_cut] * -1
        else:
            self.horizontal_channel = test.hor_channel.copy()[to_cut:-to_cut]
            # self.horizontal_cutted = test.hor_channel_raw.copy()[to_cut:-to_cut]
        # amplitude = self.horizontal_channel.max() - self.horizontal_channel.min()

        self.stimuli_channel = test.hor_stimuli.copy()[to_cut:-to_cut]
        # self.stimuli_channel -= self.stimuli_channel.mean()
        # self.stimuli_channel *= amplitude * 2
        # self.stimuli_cutted = test.hor_stimuli_raw.copy()[to_cut:-to_cut]

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
        # centered_channel = helpers.center_signal(self.horizontal_cutted)
        # centered_stimuli = helpers.center_signal(self.stimuli_cutted)
        # scaled_channel = helpers.scale_signal(centered_channel, self.angle)
        # scaled_stim_channel = helpers.scale_signal(centered_stimuli, self.angle)

        # denoised_channel = denoise_35(scaled_channel)

        # peaks_channel = signal.find_peaks_cwt(abs(denoised_channel), 1000)[:-1]

        peaks_channel = signal.find_peaks_cwt(abs(self.horizontal_channel), 1000)[:-1]
        peaks_stim_channel = signal.find_peaks_cwt(abs(self.stimuli_channel), 1000)[:-1]

        #print("Forma de hor_channel:", peaks_channel.shape)
        #print("Forma de stim_channel:", peaks_stim_channel.shape)

        if len(peaks_channel) == len(peaks_stim_channel):
            displacements = peaks_stim_channel - peaks_channel
        else:
            peaks_channel_adj = to_match(peaks_channel, peaks_stim_channel)
            displacements = peaks_stim_channel - peaks_channel_adj

        latency_res = int(round(displacements.mean(), 0))

        return latency_res / 1000.0

    @cached_property
    def saccades(self) -> list[Saccade]:
        """Saccades

        Returns:
            list[Saccade]: saccades
        """
        return [
            Saccade(
                onset=start,
                offset=end,
            )
            for start, end in saccades(self.horizontal_channel, self.angle)
        ]

    @property
    def corrective_saccades_count(self) -> int:
        """Corrective saccades count

        Returns:
            int: number of saccades
        """
        return len(self.saccades)

    @property
    def velocity_mean(self) -> float:
        """Velocity Mean

        Returns:
            float: velocity (in degrees per second)
        """
        # ch_filtered = medfilt(self.horizontal_channel, 201)
        ch_f_vel = differentiate(self.horizontal_channel)
        mean_pursuit = abs(ch_f_vel.mean())
        return mean_pursuit

    @property
    def velocity_ratio(self) -> float:
        """Velocity Ratio

        Returns:
            float: velocity Ratio
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
        #coherence_factor = (1 - c)[:10].mean()
        coherence_factor = c[:10].mean()

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
            "velocity_gain": self.velocity_ratio,
            "spectral_coherence": self.spectral_coherence,
        }

    # def save_to(self, filename: str):
    #    raise NotImplementedError()


BASE_PATH = "/Users/alison/universidad/TFG/july2024-fixed"
PURSUIT_PATH = Path(BASE_PATH) / "pursuits"

# TODO: Eliminar los que tengan error de calbración >= 50%

PURSUIT_STUDIES = [
    "Prueba_Persecucion_01.oeog",
    "Prueba_Persecucion_02.oeog",
    "Prueba_Persecucion_06.oeog",
    "Prueba_Persecucion_07.oeog",
    "Prueba_Persecucion_08.oeog",
    "Prueba_Persecucion_09.oeog",
    "Prueba_Persecucion_10.oeog",
    "Prueba_Persecucion_11.oeog",
    "Prueba_Persecucion_12.oeog",
    "Prueba_Persecucion_13.oeog",
    "Prueba_Persecucion_14.oeog",
    "Prueba_Persecucion_15.oeog",
    "Prueba_Persecucion_18.oeog",
    "Prueba_Persecucion_20.oeog",
    "Prueba_Persecucion_21.oeog",
    "Prueba_Persecucion_24.oeog",
    "Prueba_Persecucion_25.oeog",
    "Prueba_Persecucion_26.oeog",
    "Prueba_Persecucion_27.oeog",
    "Prueba_Persecucion_29.oeog",
    "Prueba_Persecucion_30.oeog",
    "Prueba_Persecucion_31.oeog",
    "Prueba_Persecucion_32.oeog",
    "Prueba_Persecucion_34.oeog",
    "Prueba_Persecucion_35.oeog",
]

OUTPUT_PATH = 'pursuits_biomarkers.xlsx'


def process_study(study: Study, pursuit: bool = False):
    test: Test
    pursuit_tests = []
    i = 1
    while i < len(study) - 1:
        pursuit_tests.append(PursuitBiomarkers(study[i], 100, False))
        i += 1
    return pursuit_tests


def save_to(pursuit_biomarker: [PursuitBiomarkers], file_name: str):
    data = tablib.Dataset(headers=['Wave Form MSE',
                                   'Latency Mean',
                                   'Corrective Saccades Count',
                                   'Velocity Mean',
                                   'Velocity Ratio',
                                   'Spectral Coherence'])
    for i in pursuit_biomarker:
        row = [i.waveform_mse[1],
               i.latency_mean,
               i.corrective_saccades_count,
               i.velocity_mean,
               i.velocity_ratio,
               i.spectral_coherence]
        data.append(row)

    with open(file_name, 'wb') as f:
        f.write(data.export('xlsx'))


if __name__ == "__main__":
    PURSUIT_OUTPUT_PATH = PURSUIT_PATH
    # PURSUIT_OUTPUT_PATH = PURSUIT_PATH / OUTPUT_PATH
    if not PURSUIT_OUTPUT_PATH.exists():
        PURSUIT_OUTPUT_PATH.mkdir(parents=True)
    res = []
    for filename in tqdm(
            PURSUIT_STUDIES,
            desc="Processing pursuit studies",
    ):
        print(f"Processing study {filename}")
        fullpath = PURSUIT_PATH / filename
        if fullpath.exists():
            study = load_study(fullpath)
            pursuits_res = process_study(study, pursuit=True)
            for i in range(2):
                res.append(pursuits_res[i])

    save_to(res, OUTPUT_PATH)

            # output_path = PURSUIT_OUTPUT_PATH / filename
            # save_study(study, output_path)

    print()