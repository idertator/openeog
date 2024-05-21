from dataclasses import dataclass
from bsp.core.differentiation import differentiate
from bsp.core.impulses import impulses
from scipy.signal import medfilt
from enum import Enum
from numpy import ndarray
import numpy as np

# CONSTANTS
SAMPLES_INTERVAL = 1/1000

class Direction(Enum):
    Same = "same"
    Left = "left"
    Right = "right"


class Size(Enum):
    Invalid = "inv"
    Small = "small"
    Large = "large"


class Movement(Enum):
    Saccade = "saccade"
    Antisaccade = "antisaccade"

@dataclass
class Event:
    onset: int
    offset: int
    direction: Direction
    size: Size
    duration: int
    amplitude: float
    transition_index: int
    transition_change_index: int
    transition_direction: Direction
    movement: Movement

    def __str__(self):
        return f"{self.transition_index} - {self.size} - {self.movement}"

@dataclass
class AntissaccadeBiomarkers:
    latency: float
    location_memory: float
    peak_velocity: float
    duration: float
    correction_latency: float

@dataclass
class AntissaccadicBiomarkers:
    antisaccades: list[AntissaccadeBiomarkers]
    latency_mean: float
    latency_std: float
    location_memory_mean: float
    location_memory_std: float
    peak_velocity_mean: float
    peak_velocity_std: float
    duration_mean: float
    duration_std: float
    correction_latency_mean: float
    correction_latency_std: float
    response_inhibition: float



def antissacadic_biomarkers(channel: np.ndarray, stimuli: np.ndarray) -> AntissaccadicBiomarkers:
    antisaccades_movements = antisaccades(channel, stimuli)
    saccades_movements = saccades(channel, stimuli, antisaccades_movements)

    latencies = antisaccade_latencies_biomarker(stimuli, antisaccades_movements)
    inhibition = antisaccade_response_inhibition_biomarker(saccades_movements, antisaccades_movements)
    location_memory = antisaccade_location_memory_biomarker(channel, stimuli, antisaccades_movements)
    velocities = antisaccade_velocities_biomarker(channel, antisaccades_movements)
    durations = antisaccade_durations_biomarker(antisaccades_movements)
    correction_latencies = antisaccade_correction_latencies_biomarker(saccades_movements, antisaccades_movements)

    pass


# Biomarcador 1
def antisaccade_latencies_biomarker(events: Iterator[Event]) -> list[float]:

    for event in events:
        if event.
    
    latencies = []
    stimuli_changes = detect_changes(stimuli)
    for start, end in antisaccades:
        last_stimuli = max(change for change in stimuli_changes if change < start)
        latency = (start - last_stimuli) * SAMPLES_INTERVAL
        latencies.append(latency)
    return latencies

# Biomarcador 2
def antisaccade_response_inhibition_biomarker(saccades_movements: list[tuple[int, int]], antisaccades_movements: list[tuple[int, int]]  ) -> float:
    return len(saccades_movements)/len(antisaccades_movements)

# Biomarcador 3
def antisaccade_location_memory_biomarker(channel: np.ndarray, stimuli: np.ndarray, antisaccades_movements:list[tuple[int, int]]) -> list[float]:
    accuracy_locations_memory = []
    amplitude_stimuli = abs(min(stimuli) - max(stimuli))

    for start, end in antisaccades_movements:
        amplitude_channel = max(abs(max(channel[start:end])), abs(min(channel[start:end]))) - min(abs(max(channel[start:end])), abs(min(channel[start:end])))
        location_memory = (amplitude_stimuli - amplitude_channel)/amplitude_stimuli
        accuracy_locations_memory.append(location_memory)
    return accuracy_locations_memory

# Biomarcador 4
def antisaccade_velocities_biomarker(channel: np.ndarray, antisaccades: list[tuple[int, int]]) -> list[float]:
    # No se aplica filtro a la velocidad
    velocities = []
    for start, end in antisaccades:
        velocidad_max = max(abs(differentiate(channel[start:end])))
        velocities.append(velocidad_max)
    return velocities

# Biomarcador 5
def antisaccade_durations_biomarker(antisaccades: list[tuple[int, int]]) -> list[float]:
    durations = []
    samples_interval = 1/1000
    for start, end in antisaccades:
        duration = (end - start) * samples_interval
        durations.append(duration)
    return durations

# Biomarcador 6 -> Ahora: Devuelve una lista de 3 elementos
def antisaccade_correction_latencies_biomarker(saccades_movements: list[tuple[int, int]], antisaccades_movements: list[tuple[int, int]]) -> list[float]:
    correction_latencies = []
    
    for start_microsaccade, end_microsaccade in saccades_movements:
        next_antisaccade_start = None
        for start_antisaccade, end_antisaccade in antisaccades_movements:
            if start_antisaccade > end_microsaccade:
                next_antisaccade_start = start_antisaccade
                break
        if next_antisaccade_start is not None:
            correction_latencies.append((start_antisaccade - end_microsaccade) * SAMPLES_INTERVAL)
    return correction_latencies