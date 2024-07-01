from .enums import Device


class Hardware:
    def __init__(
        self,
        device: Device,
        sampling_rate: int,
    ):
        self.device = device
        self.sampling_rate = sampling_rate

    @property
    def json(self) -> dict:
        return {
            "device": self.device.value,
            "sampling_rate": self.sampling_rate,
        }
