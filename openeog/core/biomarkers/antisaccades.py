from functools import cached_property
from typing import Iterator

import numpy as np
from scipy import signal

from openeog.core import differentiation, helpers
from openeog.core.models import AntiSaccade, Direction, Saccade, Size, Test
from openeog.core.stimuli import SaccadicStimuliTransitions


class AntisaccadicBiomarkers:
    def __init__(
        self,
        test: Test,
        to_cut: int = 100,
        velocity_threshold: float = 15.0,
        duration_threshold: int = 15,
        sampling_frequency: float = 1000.0,
        **kwargs,
    ):
        """Constructor

        Args:
            test (Test): test
            to_cut (int, optional): number of samples to cut. Defaults to 100.
            velocity_threshold (float, optional): velocity threshold. Defaults to 15.0.
            duration_threshold (int, optional): duration threshold. Defaults to 15.
            sampling_frequency (float, optional): sampling frequency. Defaults to 1000.0.

        Returns:
            AntisaccadicBiomarkers: object
        """
        self.angle = test.angle
        self.step = 1 / sampling_frequency
        self.velocity_threshold = velocity_threshold
        self.duration_threshold = duration_threshold

        # Cortamos muestras iniciales y finales para evitar ruidos indeseables
        cutted_hori_channel = test.hor_channel_raw[to_cut:-to_cut]
        cutted_stim_channel = test.hor_stimuli_raw[to_cut:-to_cut]

        # Escalamos a los grados de la prueba antisacádica
        # TODO: Escalar con el coeficiente de calibración
        scaled_hori_channel = helpers.scale_signal(cutted_hori_channel, self.angle)
        scaled_stim_channel = helpers.scale_signal(cutted_stim_channel, self.angle)

        # Centramos las 2 señales para que esten en el mismo espacio angular
        centered_hori_channel = helpers.center_signal(scaled_hori_channel)
        self.centered_stim_channel = helpers.center_signal(scaled_stim_channel)

        # Eliminación de ruido de la señal horizontal
        self.denoised_hori_channel = helpers.denoise_35(centered_hori_channel)

        # Cálculo del perfil de velocidad
        vel_channel = differentiation.differentiate(self.denoised_hori_channel)
        self.abs_vel_channel = abs(vel_channel)

        # Crando objeto de estímulo
        self.stimuli_transitions = SaccadicStimuliTransitions(
            self.centered_stim_channel
        )

    def _iterate_impulses(self) -> Iterator[tuple[int, int]]:
        """Iterate over impulses

        Yields:
            Iterator[tuple[int, int]]: (onset, offset)
        """
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
        """Clasify impulses

        Yields:
            Iterator[tuple[int, int, Direction, Size, int, float]]: (onset, offset, direction, size, duration, amplitude)
        """
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

    def _detect_all_annotations(self) -> Iterator[Saccade | AntiSaccade]:
        """Detect all annotations

        Yields:
            Iterator[Saccade | AntiSaccade]: annotation
        """
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
                latency=onset - t_change_before,
                duration=duration,
                amplitude=amplitude,
                deviation=amplitude / self.angle,
                peak_velocity=self.abs_vel_channel[onset:offset].max(),
                transition_index=t_idx,
                transition_change_index=t_change,
                transition_change_before_index=t_change_before,
                transition_direction=t_direction,
                direction=direction,
                size=size,
            )

    # Eventos

    @cached_property
    def annotations(self) -> list[Saccade | AntiSaccade]:
        """Annotations

        Returns:
            list[Saccade | AntiSaccade]: annotations
        """
        result = [annotation for annotation in self._detect_all_annotations()]

        result = []
        for idx, annotation in enumerate(result):
            if annotation.size == Size.Large and isinstance(annotation, AntiSaccade):
                # Es una antisácada válida por lo que la lanzamos
                result.append(annotation)
                continue

            if annotation.size == Size.Small and isinstance(annotation, Saccade):
                if idx == len(result) - 1:
                    # Es el último evento por lo tanto nos la saltamos
                    continue

                next_event = result[idx + 1]
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

    @cached_property
    def antisaccades(self) -> list[AntiSaccade]:
        """Antisaccades

        Returns:
            list[AntiSaccade]: antisaccades
        """
        return [
            annotation
            for annotation in self.annotations
            if isinstance(annotation, AntiSaccade)
        ]

    @cached_property
    def saccades(self) -> list[Saccade]:
        """Saccades

        Returns:
            list[Saccade]: saccades
        """
        return [
            annotation
            for annotation in self.annotations
            if isinstance(annotation, Saccade)
        ]

    # Biomarcadores temporales

    @cached_property
    def _latencies(self) -> np.ndarray:
        """Antisaccades latencies

        Returns:
            np.ndarray: latencies
        """
        return np.array(
            [antisaccade.latency * self.step for antisaccade in self.antisaccades]
        )

    @cached_property
    def latency_mean(self) -> float:
        """Antisaccades latency mean

        Returns:
            float: latency
        """
        return float(self._latencies.mean()) if self._latencies.any() else 0.0

    @cached_property
    def latency_std(self) -> float:
        """Antisaccades latency std

        Returns:
            float: latency
        """
        return float(self._latencies.std()) if self._latencies.any() else 0.0

    @cached_property
    def _correction_latencies(self) -> np.ndarray:
        """Correction latencies

        Returns:
            np.ndarray: correction latencies
        """
        correction_latencies = []
        previous_annotation = None

        for annotation in self.annotations:
            if previous_annotation is None:
                correction_latencies.append(0)

            elif (
                previous_annotation is not None
                and isinstance(previous_annotation, Saccade)
                and isinstance(annotation, AntiSaccade)
                and annotation.transition_index == previous_annotation.transition_index
            ):
                correction_latency = (
                    annotation.onset - previous_annotation.offset
                ) * self.step
                correction_latencies.append(correction_latency)

            elif (
                previous_annotation is not None
                and not isinstance(previous_annotation, Saccade)
                and isinstance(annotation, AntiSaccade)
            ):
                correction_latencies.append(0)

            previous_annotation = annotation

        return np.array(correction_latencies)

    @property
    def correction_latency_mean(self) -> float:
        """Correction latency mean

        Returns:
            float: correction latency
        """
        return (
            float(self._correction_latencies.mean())
            if self._correction_latencies.any()
            else 0.0
        )

    @property
    def correction_latency_std(self) -> float:
        """Correction latency std

        Returns:
            float: correction latency
        """
        return (
            float(self._correction_latencies.std())
            if self._correction_latencies.any()
            else 0.0
        )

    @cached_property
    def _durations(self) -> np.ndarray:
        """Antisaccades durations

        Returns:
            np.ndarray: durations
        """
        return np.array(
            [antisaccade.duration * self.step for antisaccade in self.antisaccades]
        )

    @cached_property
    def duration_mean(self) -> float:
        """Antisaccades duration mean

        Returns:
            float: duration
        """
        return float(self._durations.mean()) if self._durations.any() else 0.0

    @cached_property
    def duration_std(self) -> float:
        """Antisaccades duration std

        Returns:
            float: duration
        """
        return float(self._durations.std()) if self._durations.any() else 0.0

    # Biomarcadores espaciales

    @cached_property
    def _accuracy_locations_memory(self) -> np.ndarray:
        """Accuracy locations memory

        Returns:
            np.ndarray: accuracy locations memory
        """
        accuracy_locations_memory = []
        amplitude_stimuli = (
            abs(min(self.centered_stim_channel) - max(self.centered_stim_channel)) / 2
        )
        for antisaccade in self.antisaccades:
            onset_value = self.denoised_hori_channel[antisaccade.onset]
            offset_value = self.denoised_hori_channel[antisaccade.offset]
            amplitude = abs(offset_value - onset_value)

            location_memory = abs(amplitude_stimuli - amplitude) / amplitude_stimuli
            accuracy_locations_memory.append(location_memory)

        return np.array(accuracy_locations_memory)

    @cached_property
    def memory_mean(self) -> float:
        """Accuracy locations memory mean

        Returns:
            float: accuracy locations memory
        """
        return (
            float(self._accuracy_locations_memory.mean())
            if self._accuracy_locations_memory.any()
            else 0.0
        )

    @cached_property
    def memory_std(self) -> float:
        """Accuracy locations memory std

        Returns:
            float: accuracy locations memory
        """
        return (
            float(self._accuracy_locations_memory.std())
            if self._accuracy_locations_memory.any()
            else 0.0
        )

    # Biomarcadores cinéticos

    @cached_property
    def _peak_velocities(self) -> np.ndarray:
        """Antisaccades peak velocities

        Returns:
            np.ndarray: peak velocities
        """
        return np.array(
            [antisaccade.peak_velocity for antisaccade in self.antisaccades]
        )

    @cached_property
    def velocity_peak_mean(self) -> float:
        """Antisaccades peak velocity mean

        Returns:
            float: peak velocity
        """
        return (
            float(self._peak_velocities.mean()) if self._peak_velocities.any() else 0.0
        )

    @cached_property
    def velocity_peak_std(self) -> float:
        """Antisaccades peak velocity std

        Returns:
            float: peak velocity
        """
        return (
            float(self._peak_velocities.std()) if self._peak_velocities.any() else 0.0
        )

    # Biomarcadores específicos puros

    @cached_property
    def response_inhibition(self) -> float:
        """Response inhibition

        Returns:
            float: Ratio between total of saccades over total of antisaccades
        """
        saccades_count = len(self.saccades)
        antisaccades_count = len(self.antisaccades)

        if antisaccades_count:
            return saccades_count / antisaccades_count

        return 0.0

    @property
    def to_dict(self) -> dict[str, int | float]:
        """To Dict

        Returns:
            dict[str, int | float]: dictionary
        """
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

    def save_to(self, filename: str):
        raise NotImplementedError()
