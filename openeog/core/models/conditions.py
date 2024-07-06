class Conditions:
    def __init__(
        self,
        light_intensity: float = 0.0,
        errors: int = 0,
    ):
        self.light_intensity = light_intensity
        self.errors = errors

    @property
    def json(self) -> dict:
        return {
            "light_intensity": self.light_intensity,
            "errors": self.errors,
        }
