from bsp.core.models.enums import AnnotationType, Direction, Size

from .base import Annotation


class Saccade(Annotation):
    def __init__(
        self,
        onset: int,
        offset: int,
        latency: int = 0,
        duration: int = 0,
        amplitude: float = 0.0,
        deviation: float = 0.0,
        peak_velocity: float = 0.0,
        transition_index: int = -1,
        transition_change_index: int = -1,
        transition_change_before_index: int = -1,
        transition_direction: Direction = Direction.Same,
        direction: Direction = Direction.Same,
        size: Size = Size.Invalid,
    ):
        super().__init__(
            annotation_type=AnnotationType.Saccade,
            onset=onset,
            offset=offset,
        )
        self.direction = direction
        self.size = size
        self.latency = latency
        self.duration = duration
        self.amplitude = amplitude
        self.deviation = deviation
        self.peak_velocity = peak_velocity
        self.transition_index = transition_index
        self.transition_change_index = transition_change_index
        self.transition_change_before_index = transition_change_before_index
        self.transition_direction = transition_direction

    @property
    def json(self) -> dict:
        return {
            **super().json,
            "direction": self.direction.value,
            "size": self.size.value,
            "latency": self.latency,
            "duration": self.duration,
            "amplitude": self.amplitude,
            "deviation": self.deviation,
            "peak_velocity": self.peak_velocity,
            "transition_index": self.transition_index,
            "transition_change_index": self.transition_change_index,
            "transition_change_before_index": self.transition_change_before_index,
            "transition_direction": self.transition_direction.value,
        }
