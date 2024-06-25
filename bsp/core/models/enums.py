from enum import Enum


class Direction(str, Enum):
    Same = "same"
    Left = "left"
    Right = "right"


class Size(str, Enum):
    Invalid = "inv"
    Small = "small"
    Large = "large"


class Protocol(str, Enum):
    Saccadic = "saccadic"
    Pursuit = "pursuit"
    Antisaccadic = "antisaccadic"

    @property
    def name(self) -> str:
        match self:
            case Protocol.Saccadic:
                return "Protocolo Sacádico"

            case Protocol.Pursuit:
                return "Protocolo de Persecución"

            case Protocol.Antisaccadic:
                return "Protocolo Antisacádico"


class TestType(str, Enum):
    HorizontalCalibration = "HorizontalCalibration"
    HorizontalSaccadic = "HorizontalSaccadic"
    VerticalCalibration = "VerticalCalibration"
    HorizontalPursuit = "HorizontalPursuit"
    HorizontalAntisaccadic = "HorizontalAntisaccadic"
    VerticalAntisaccadic = "VerticalAntisaccadic"

    @property
    def name(self) -> str:
        match self:
            case TestType.HorizontalCalibration:
                return "Calibración Horizontal"

            case TestType.HorizontalSaccadic:
                return "Sacádica"

            case TestType.VerticalCalibration:
                return "Calibración Vertical"

            case TestType.HorizontalPursuit:
                return "Persecución Horizontal"

            case TestType.HorizontalAntisaccadic:
                return "Antisacádica Horizontal"

            case TestType.VerticalAntisaccadic:
                return "Antisacádica Vertical"

        return "Desconocida"


class AnnotationType(str, Enum):
    Fixation = "Fixation"
    Saccade = "Saccade"
    Pursuit = "Pursuit"
    AntiSaccade = "AntiSaccade"

    @property
    def name(self) -> str:
        match self:
            case AnnotationType.Fixation:
                return "Fijación"

            case AnnotationType.Saccade:
                return "Sácada"

            case AnnotationType.Pursuit:
                return "Persecución"

            case AnnotationType.AntiSaccade:
                return "AntiSaccade"

        return "Desconocida"
