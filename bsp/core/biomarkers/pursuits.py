from bsp.core.models import Test

# from functools import cached_property
#
# from numpy import ndarray


class PursuitBiomarkers:
    def __init__(
        self,
        test: Test,
        samples_to_cut: int,
        **kwargs,
    ):
        self.test = test
        self.samples_to_cut = samples_to_cut

    def _preprocess_signals(self):
        pass

    # @cached_property
    # def _filetered_velocity(self) -> ndarray:
    #     return filtro(self.test.hor_channel_raw)

    @property
    def waveform_mse(self) -> float:
        raise NotImplementedError()

    @property
    def latency_mean(self) -> float:
        # En segundos
        raise NotImplementedError()

    @property
    def corrective_saccades_count(self) -> int:
        raise NotImplementedError()

    @property
    def velocity_mean(self) -> float:
        raise NotImplementedError()
        # velocities = self._filetered_velocity

    @property
    def velocity_gain(self) -> float:
        raise NotImplementedError()
        # velocities = self._filetered_velocity

    @property
    def spectral_coherence(self) -> float:
        raise NotImplementedError()

    @property
    def to_dict(self) -> dict[str, int | float]:
        return {
            "waveform_mse": self.waveform_mse,
            "latency_mean": self.latency_mean,
            "corrective_saccades_count": self.corrective_saccades_count,
            "velocity_mean": self.velocity_mean,
            "velocity_gain": self.velocity_gain,
            "spectral_coherence": self.spectral_coherence,
        }
