from functools import cached_property
from typing import Iterator

import numpy as np
from scipy import signal

from bsp.core.denoising import denoise_35
from bsp.core.differentiation import differentiate
from bsp.core.models import AntiSaccade, Direction, Saccade, Size, Test
from bsp.core.stimuli import SaccadicStimuliTransitions

from .utils import center_signal, scale_channel

# CONSTANTS
SAMPLES_INTERVAL = 1 / 1000


class AntisaccadicBiomarkers:
    def __init__(
        self,
        test: Test,
        samples_to_cut: int = 100,
        velocity_threshold: float = 15.0,
        duration_threshold: int = 15,
        **kwargs,
    ):
        self.test = test
        self.samples_to_cut = samples_to_cut
        self.velocity_threshold = velocity_threshold
        self.duration_threshold = duration_threshold

        # Cortamos muestras iniciales y finales para evitar ruidos indeseables
        self.cutted_hori_channel = test.hor_channel_raw[samples_to_cut:-samples_to_cut]
        self.cutted_stim_channel = test.hor_stimuli_raw[samples_to_cut:-samples_to_cut]
        self.time_channel = np.arange(len(self.cutted_hori_channel))

        # Escalamos a los grados de la prueba antisacádica
        # TODO: Escalar con el coeficiente de calibración
        self.scaled_hori_channel = scale_channel(
            self.cutted_hori_channel, self.test.angle
        )
        self.scaled_stim_channel = scale_channel(
            self.cutted_stim_channel, self.test.angle
        )

        # Centramos las 2 señales para que esten en el mismo espacio angular
        self.centered_hori_channel = center_signal(self.scaled_hori_channel)
        self.centered_stim_channel = center_signal(self.scaled_stim_channel)

        # Eliminación de ruido de la señal horizontal
        self.denoised_hori_channel = denoise_35(self.centered_hori_channel)

        # Cálculo del perfil de velocidad
        self.vel_channel = differentiate(self.denoised_hori_channel)
        self.abs_vel_channel = abs(self.vel_channel)

        # Crando objeto de estímulo
        self.stimuli_transitions = SaccadicStimuliTransitions(
            self.centered_stim_channel
        )

    def _iterate_impulses(
        self,
    ) -> Iterator[tuple[int, int]]:
        channel = self.abs_vel_channel
        peaks = signal.find_peaks_cwt(channel, 30)

        for peak in peaks:
            onset = peak
            while onset > 0 and channel[onset - 1] >= self.velocity_threshold:
                onset -= 1

            offset = peak
            while (
                offset < len(channel) - 1
                and channel[offset + 1] >= self.velocity_threshold
            ):
                offset += 1

            if offset - onset >= self.duration_threshold:
                yield onset, offset

    def _clasify_impulses(
        self,
    ) -> Iterator[tuple[int, int, Direction, Size, int, float]]:
        # Onset, Offset, Direction, Size, Duration, Amplitude
        already_yielded = set()

        for onset, offset in self._iterate_impulses():
            duration = offset - onset

            onset_angle = self.denoised_hori_channel[onset]
            offset_angle = self.denoised_hori_channel[offset]

            amplitude = abs(offset_angle - onset_angle)
            if onset_angle < offset_angle:
                direction = Direction.Right
            elif onset_angle > offset_angle:
                direction = Direction.Left
            else:
                direction = Direction.Same

            if amplitude < 1.0:
                continue
            elif amplitude < 5.0:
                size = Size.Small
            else:
                size = Size.Large

            if (onset, offset) not in already_yielded:
                already_yielded.add((onset, offset))
            else:
                continue

            yield onset, offset, direction, size, duration, amplitude

    def _detect_all_annotations(
        self,
    ) -> Iterator[Saccade | AntiSaccade]:
        for (
            onset,
            offset,
            direction,
            size,
            duration,
            amplitude,
        ) in self._clasify_impulses():
            t_idx, t_change, t_change_before, t_direction = self.stimuli_transitions[
                onset
            ]

            if direction == t_direction:
                Movement = Saccade
            else:
                Movement = AntiSaccade

            yield Movement(
                onset=onset,
                offset=offset,
                latency=onset - t_change,
                duration=duration,
                amplitude=amplitude,
                deviation=amplitude / self.test.angle,
                peak_velocity=self.abs_vel_channel[onset:offset].max(),
                transition_index=t_idx,
                transition_change_index=t_change,
                transition_change_before_index=t_change_before,
                transition_direction=t_direction,
                direction=direction,
                size=size,
            )

    @cached_property
    def detect_annotations(self) -> list[Saccade | AntiSaccade]:
        annotations = [annotation for annotation in self._detect_all_annotations()]

        result = []
        for idx, annotation in enumerate(annotations):
            if annotation.size == Size.Large and isinstance(annotation, AntiSaccade):
                # Es una antisácada válida por lo que la lanzamos
                result.append(annotation)
                continue

            if annotation.size == Size.Small and isinstance(annotation, Saccade):
                if idx == len(annotations) - 1:
                    # Es el último evento por lo tanto nos la saltamos
                    continue

                next_event = annotations[idx + 1]
                if annotation.transition_index != next_event.transition_index:
                    # El evento y el siguiente no están en la misma transición de estímulo por lo que nos la saltamos
                    continue

                if next_event.size == Size.Large and isinstance(
                    next_event, AntiSaccade
                ):
                    # El siguiente evento es una antisácada correcta
                    # Por lo que hace que el movimiento sea un movimiento correctivo correcto
                    # Por lo tanto se lanza también
                    result.append(annotation)

        return result

    # def annotate_test(self):
    #     # Identificar todas las anotaciones presentes en la señal y guardarlas en self.annotations
    #     raise NotImplementedError()
    #


#     @property
#     def latency_mean(self) -> float:
#         latencies = np.array([saccade.latency for saccade in self.annotations])
#         return latencies.mean()
#
#     @property
#     def latency_std(self) -> float:
#         # En segundos
#         raise NotImplementedError()
#
#     @property
#     def memory_mean(self) -> float:
#         # Ángulo en grados
#         raise NotImplementedError()
#
#     @property
#     def memory_std(self) -> float:
#         # Ángulo en grados
#         raise NotImplementedError()
#
#     @property
#     def velocity_peak_mean(self) -> float:
#         # Ángulo en grados por segundo
#         raise NotImplementedError()
#
#     @property
#     def velocity_peak_std(self) -> float:
#         # Ángulo en grados por segundo
#         raise NotImplementedError()
#
#     @property
#     def duration_mean(self) -> float:
#         # Ángulo en grados por segundo
#         raise NotImplementedError()
#
#     @property
#     def duration_std(self) -> float:
#         # Ángulo en grados por segundo
#         raise NotImplementedError()
#
#     @property
#     def correction_latency_mean(self) -> float:
#         # Ángulo en grados por segundo
#         raise NotImplementedError()
#
#     @property
#     def correction_latency_std(self) -> float:
#         # Ángulo en grados por segundo
#         raise NotImplementedError()
#
#     @property
#     def response_inhibition(self) -> float:
#         # Ratio entre total de sácadas inapropiadas / total de antisácadas
#         raise NotImplementedError()
#
#     @property
#     def to_dict(self) -> dict[str, int | float]:
#         return {
#             "latency_mean": self.latency_mean,
#             "latency_std": self.latency_std,
#             "memory_mean": self.memory_mean,
#             "memory_std": self.memory_std,
#             "velocity_peak_mean": self.velocity_peak_mean,
#             "velocity_peak_std": self.velocity_peak_std,
#             "duration_mean": self.duration_mean,
#             "duration_std": self.duration_std,
#             "correction_latency_mean": self.correction_latency_mean,
#             "correction_latency_std": self.correction_latency_std,
#             "response_inhibition": self.response_inhibition,
#         }
#
#
# # Biomarcador 1
# def antisaccade_latencies_biomarker(events: Iterator[Event]) -> list[float]:
#     latencies = []
#     for event in events:
#         if event.movement == Movement.Antisaccade:
#             latency = (
#                 event.onset - event.transition_change_before_index
#             ) * SAMPLES_INTERVAL
#             latencies.append(latency)
#     return latencies
#
#
# # Biomarcador 2
# def antisaccade_response_inhibition_biomarker(events: Iterator[Event]) -> float:
#     num_saccades_movements = 0
#     num_antisaccades_movements = 0
#     for event in events:
#         if event.movement == Movement.Antisaccade:
#             num_antisaccades_movements += 1
#         if event.movement == Movement.Saccade:
#             num_saccades_movements += 1
#     return num_saccades_movements / num_antisaccades_movements
#
#
# # Biomarcador 3
# def antisaccade_location_memory_biomarker(
#     channel: np.ndarray, stimuli: np.ndarray, events: Iterator[Event]
# ) -> list[float]:
#     accuracy_locations_memory = []
#     amplitude_stimuli = abs(min(stimuli) - max(stimuli)) / 2
#     for event in events:
#         if event.movement == Movement.Antisaccade:
#             amplitude_channel = max(
#                 abs(max(channel[event.onset : event.offset])),
#                 abs(min(channel[event.onset : event.offset])),
#             ) - min(
#                 abs(max(channel[event.onset : event.offset])),
#                 abs(min(channel[event.onset : event.offset])),
#             )
#             location_memory = (
#                 abs(amplitude_stimuli - amplitude_channel) / amplitude_stimuli
#             )
#             print(amplitude_stimuli, amplitude_channel)
#             accuracy_locations_memory.append(location_memory)
#     return accuracy_locations_memory
#
#
# # Biomarcador 4
# def antisaccade_velocities_biomarker(
#     channel: np.ndarray, events: Iterator[Event]
# ) -> list[float]:
#     velocities = []
#     for event in events:
#         if event.movement == Movement.Antisaccade:
#             velocidad_max = max(abs(differentiate(channel[event.onset : event.offset])))
#             velocities.append(velocidad_max)
#     return velocities
#
#
# # Biomarcador 5
# def antisaccade_durations_biomarker(events: Iterator[Event]) -> list[float]:
#     durations = []
#     for event in events:
#         if event.movement == Movement.Antisaccade:
#             duration = (event.offset - event.onset) * SAMPLES_INTERVAL
#             durations.append(duration)
#     return durations
#
#
# # Biomarcador 6 -> Ahora: Devuelve una lista de 3 elementos
# def antisaccade_correction_latencies_biomarker(
#     saccades_movements: list[tuple[int, int]],
#     antisaccades_movements: list[tuple[int, int]],
# ) -> list[float]:
#     # Se crea una lista porque se necesita un valor del evento anterior
#     def create_list_event(events: Iterator[Event]):
#         list = []
#         for event in events:
#             list.append(event)
#         return list
#
#     correction_latencies = []
#     for idx, event in enumerate(create_list_event(events)):
#         if (
#             events[idx - 1].movement == Movement.Saccade
#             and event.movement == Movement.Antisaccade
#             and event.transition_index == events[idx - 1].transition_index
#         ):
#             correction_latency = (
#                 events[idx].onset - events[idx - 1].offset
#             ) * SAMPLES_INTERVAL
#             correction_latencies.append(correction_latency)
#             saccade_has_ocurred = False
#         elif (
#             events[idx - 1].movement != Movement.Saccade
#             and event.movement == Movement.Antisaccade
#         ):
#             correction_latencies.append(0)
#     return correction_latencies
#

