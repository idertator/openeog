# from functools import cached_property
from typing import Iterator

from numpy import array

from bsp.core.models import Antisaccade, Saccade, Test


class AntisaccadicBiomarkers:
    def __init__(
        self,
        test: Test,
        samples_to_cut: int,
        **kwargs,
    ):
        self.test = test
        self.samples_to_cut = samples_to_cut
        self.annotations: list[Saccade | Antisaccade] = []

        self.horizontal_channel = None
        self.stimuli_channel = None

        self._preprocess_signals()

    def _preprocess_signals(self):
        cut_count = self.samples_to_cut
        self.horizontal_channel = self.test.hor_channel_raw[cut_count:-cut_count]
        self.stimuli_channel = self.test.hor_stimuli[cut_count:-cut_count]

    def _iterate_impulses(self) -> Iterator[Saccade | Saccade]:
        yield Saccade()

    def annotate_test(self):
        # Identificar todas las anotaciones presentes en la señal y guardarlas en self.annotations
        raise NotImplementedError()

    @property
    def latency_mean(self) -> float:
        latencies = array([saccade.latency for saccade in self.annotations])
        return latencies.mean()

    @property
    def latency_std(self) -> float:
        # En segundos
        raise NotImplementedError()

    @property
    def memory_mean(self) -> float:
        # Ángulo en grados
        raise NotImplementedError()

    @property
    def memory_std(self) -> float:
        # Ángulo en grados
        raise NotImplementedError()

    @property
    def velocity_peak_mean(self) -> float:
        # Ángulo en grados por segundo
        raise NotImplementedError()

    @property
    def velocity_peak_std(self) -> float:
        # Ángulo en grados por segundo
        raise NotImplementedError()

    @property
    def duration_mean(self) -> float:
        # Ángulo en grados por segundo
        raise NotImplementedError()

    @property
    def duration_std(self) -> float:
        # Ángulo en grados por segundo
        raise NotImplementedError()

    @property
    def correction_latency_mean(self) -> float:
        # Ángulo en grados por segundo
        raise NotImplementedError()

    @property
    def correction_latency_std(self) -> float:
        # Ángulo en grados por segundo
        raise NotImplementedError()

    @property
    def response_inhibition(self) -> float:
        # Ratio entre total de sácadas inapropiadas / total de antisácadas
        raise NotImplementedError()

    @property
    def to_dict(self) -> dict[str, int | float]:
        return {
            "latency_mean": self.latency_mean,
            "latency_std": self.latency_std,
            "memory_mean": self.memory_mean,
            "memory_std": self.memory_std,
            "velocity_peak_mean": self.velocity_peak_mean,
            "velocity_peak_std": self.velocity_peak_std,
            "duration_mean": self.duration_mean,
            "duration_std": self.duration_std,
            "correction_latency_mean": self.correction_latency_mean,
            "correction_latency_std": self.correction_latency_std,
            "response_inhibition": self.response_inhibition,
        }
