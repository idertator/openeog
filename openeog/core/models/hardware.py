from .enums import Device


class Hardware:
    def __init__(
        self,
        acquisition_device: Device,
        acquisition_sampling_rate: int,
        stimuli_monitor: str,
        stimuli_monitor_refresh_rate: int,
        stimuli_monitor_width: int,
        stimuli_monitor_height: int,
        stimuli_monitor_resolution_width: int,
        stimuli_monitor_resolution_height: int,
        stimuli_ball_radius: int,
    ):
        self.acquisition_device = acquisition_device
        self.acquisition_sampling_rate = acquisition_sampling_rate

        self.stimuli_monitor = stimuli_monitor
        self.stimuli_monitor_refresh_rate = stimuli_monitor_refresh_rate
        self.stimuli_monitor_width = stimuli_monitor_width
        self.stimuli_monitor_height = stimuli_monitor_height
        self.stimuli_monitor_resolution_width = stimuli_monitor_resolution_width
        self.stimuli_monitor_resolution_height = stimuli_monitor_resolution_height
        self.stimuli_ball_radius = stimuli_ball_radius

    @property
    def json(self) -> dict:
        return {
            "acquisition_device": self.acquisition_device.value,
            "acqusition_sampling_rate": self.acquisition_sampling_rate,
            "stimuli_monitor": self.stimuli_monitor,
            "stimuli_monitor_refresh_rate": self.stimuli_monitor_refresh_rate,
            "stimuli_monitor_width": self.stimuli_monitor_width,
            "stimuli_monitor_height": self.stimuli_monitor_height,
            "stimuli_monitor_resolution_width": self.stimuli_monitor_resolution_width,
            "stimuli_monitor_resolution_height": self.stimuli_monitor_resolution_height,
            "stimuli_ball_radius": self.stimuli_ball_radius,
        }
