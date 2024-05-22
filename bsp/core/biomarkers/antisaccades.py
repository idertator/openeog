from dataclasses import dataclass
from bsp.core.differentiation import differentiate
from bsp.core.impulses import impulses
from scipy.signal import medfilt
from enum import Enum
from numpy import ndarray
import numpy as np

# CONSTANTS
SAMPLES_INTERVAL = 1/1000

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


# Biomarcador 1
def antisaccade_latencies_biomarker(events: Iterator[Event]) -> list[float]:
    latencies = []
    for event in events:
        if event.movement == Movement.Antisaccade:
            latency = (event.onset - event.transition_change_before_index) * SAMPLES_INTERVAL
            latencies.append(latency)
    return latencies

# Biomarcador 2
def antisaccade_response_inhibition_biomarker(events: Iterator[Event]) -> float:
    num_saccades_movements = 0
    num_antisaccades_movements = 0
    for event in events:
        if event.movement == Movement.Antisaccade:
            num_antisaccades_movements += 1
        if event.movement == Movement.Saccade:
            num_saccades_movements += 1
    return num_saccades_movements/num_antisaccades_movements

# Biomarcador 3
def antisaccade_location_memory_biomarker(channel: np.ndarray, stimuli: np.ndarray, events: Iterator[Event]) -> list[float]:
    accuracy_locations_memory = []
    amplitude_stimuli = abs(min(stimuli) - max(stimuli))/2  
    for event in events:
        if event.movement == Movement.Antisaccade:
            amplitude_channel = max(abs(max(channel[event.onset:event.offset])), abs(min(channel[event.onset:event.offset]))) - min(abs(max(channel[event.onset:event.offset])), abs(min(channel[event.onset:event.offset])))
            location_memory = abs(amplitude_stimuli - amplitude_channel)/amplitude_stimuli
            print(amplitude_stimuli, amplitude_channel)
            accuracy_locations_memory.append(location_memory)
    return accuracy_locations_memory

# Biomarcador 4
def antisaccade_velocities_biomarker(channel: np.ndarray, events: Iterator[Event]) -> list[float]:
    velocities = []
    for event in events:
        if event.movement == Movement.Antisaccade:
            velocidad_max = max(abs(differentiate(channel[event.onset:event.offset])))
            velocities.append(velocidad_max)
    return velocities

# Biomarcador 5
def antisaccade_durations_biomarker(events: Iterator[Event]) -> list[float]:
    durations = []
    for event in events:
        if event.movement == Movement.Antisaccade:
            duration = (event.offset - event.onset) * SAMPLES_INTERVAL
            durations.append(duration)
    return durations

# Biomarcador 6 -> Ahora: Devuelve una lista de 3 elementos
def antisaccade_correction_latencies_biomarker(saccades_movements: list[tuple[int, int]], antisaccades_movements: list[tuple[int, int]]) -> list[float]:
    # Se crea una lista porque se necesita un valor del evento anterior
    def create_list_event(events: Iterator[Event]):
        list = []
        for event in events:
            list.append(event)
        return list
           
    correction_latencies = []
    for idx, event in enumerate(create_list_event(events)):
        if events[idx-1].movement == Movement.Saccade and event.movement == Movement.Antisaccade and event.transition_index == events[idx-1].transition_index:
            correction_latency = (events[idx].onset - events[idx-1].offset) * SAMPLES_INTERVAL
            correction_latencies.append(correction_latency)
            saccade_has_ocurred = False
        elif events[idx-1].movement != Movement.Saccade and event.movement == Movement.Antisaccade:
            correction_latencies.append(0)
    return correction_latencies