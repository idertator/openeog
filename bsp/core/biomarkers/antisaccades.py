from bsp.core.differentiation import differentiate
from bsp.core.impulses import impulses

import numpy as np
from enum import Enum
from numpy import ndarray

class Direction(Enum):
    Left = "left"
    Right = "right"


def saccades(channel: np.ndarray, stimuli: np.ndarray) -> list[tuple[int, int]]:
    # Impulses no encuentra las minis sácadas 
    pass 

def antisaccades(channel: np.ndarray, stimuli: np.ndarray) -> list[tuple[int, int]]:
    list = []
    samples_to_remove = 100
    stimuli = stimuli.copy()[:-samples_to_remove]
    amplitude_stimuli = abs(min(stimuli) - max(stimuli))
    min_amplitud_to_be_antisaccade = (amplitude_stimuli-1)/2
            
    for start, end in impulses(channel):
        if max(channel[start:end]) >= 0 and  min(channel[start:end]) >= 0:
            amplitude_channel = max(channel[start:end]) - min(channel[start:end])
        elif max(channel[start:end]) < 0 and min(channel[start:end]) < 0:
            amplitude_channel = abs(max(channel[start:end]) - min(channel[start:end]))
        else:
            amplitude_channel = max(abs(max(channel[start:end])), abs(min(channel[start:end]))) - min(abs(max(channel[start:end])), abs(min(channel[start:end])))
            
        if amplitude_channel > min_amplitud_to_be_antisaccade:
            list.append((start, end))
    return list

def direction(channel: np.ndarray, stimuli: np.ndarray, start: int, end: int) -> Direction:
    if channel[end] > 0:
        if stimuli[end] > 0:
            # Sácada Derecha
            return Direction.Right
        elif stimuli[end] < 0:
            # Antisácada Derecha
            return Direction.Right
    elif channel[end] < 0:
        if stimuli[end] > 0:
            # Antisácada Izquierda
            return Direction.Left
        elif stimuli[end] < 0:
            # Sácada Izquierda
            return Direction.Left

# Biomarcador 1
def antisaccade_latencies_biomarker(stimuli: np.ndarray, movements: list[tuple[int, int]]) -> list[float]:

    def detect_changes(stimuli: np.ndarray) -> list[int]:
        change_indices = []
        for i in range(1, len(stimuli)):
            if stimuli[i] != stimuli[i - 1]:
                change_indices.append(i)
        return change_indices
    
    latencies = []
    samples_interval = 1/1000
    stimuli_changes = detect_changes(stimuli)
    for start, end in movements:
        last_stimuli = max(change for change in stimuli_changes if change < start)
        latency = (start - last_stimuli) * samples_interval
        latencies.append(latency)
    return latencies

# Biomarcador 2
def antisaccade_response_inhibition_biomarker(channel: np.ndarray, stimuli: np.ndarray) -> float:
    pass

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
def antisaccade_velocities_biomarker(channel: np.ndarray, movements: list[tuple[int, int]]) -> list[float]:
    # No se aplica filtro a la velocidad
    velocities = []
    for start, end in movements:
        velocidad_max = max(abs(differentiate(channel[start:end])))
        velocities.append(velocidad_max)
    return velocities

# Biomarcador 5
def antisaccade_durations_biomarker(movements: list[tuple[int, int]]) -> list[float]:
    durations = []
    samples_interval = 1/1000
    for start, end in movements:
        duration = (end - start) * samples_interval
        durations.append(duration)
    return durations

# Biomarcador 6
def antisaccade_correction_latencies_biomarker(saccades_movements: list[tuple[int, int]], antisaccades_movements: list[tuple[int, int]]) -> list[float]:
    pass