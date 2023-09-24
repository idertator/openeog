from dataclasses import dataclass, field

from numpy import mean, std
from tablib import Dataset, Workbook

from .models import Saccade, Study, Test


@dataclass
class _Stats:
    test: str
    latencies: list[int] = field(default_factory=list)
    durations: list[int] = field(default_factory=list)
    amplitudes: list[float] = field(default_factory=list)
    deviations: list[float] = field(default_factory=list)
    peak_velocities: list[float] = field(default_factory=list)

    def add_sample(
        self,
        latency: int,
        duration: int,
        amplitude: float,
        deviation: float,
        peak_velocity: float,
    ):
        self.latencies.append(latency)
        self.durations.append(duration)
        self.amplitudes.append(amplitude)
        self.deviations.append(deviation)
        self.peak_velocities.append(peak_velocity)

    @classmethod
    def headers(cls) -> list[str]:
        return [
            "Prueba",
            "Latencia Media (ms)",
            "Latencia StD (ms)",
            "Duración Media (ms)",
            "Duración StD (ms)",
            "Amplitud Media (°)",
            "Amplitud StD (°)",
            "Desviación Media (%)",
            "Desviación StD (%)",
            "Velocidad Máxima Media (°/s)",
            "Velocidad Máxima StD (°/s)",
        ]

    @property
    def row(self) -> list[int | float]:
        return [
            self.test,
            mean(self.latencies),
            std(self.latencies),
            mean(self.durations),
            std(self.durations),
            mean(self.amplitudes),
            std(self.amplitudes),
            mean(self.deviations),
            std(self.deviations),
            mean(self.peak_velocities),
            std(self.peak_velocities),
        ]


def _test_dataset(test: Test) -> tuple[Dataset, _Stats]:
    test_name = "{test} {angle}".format(
        test=test.name,
        angle=test.angle,
    )
    ds = Dataset(
        title=test_name,
        headers=[
            "#",
            "Inicio",
            "Fin",
            "Latencia (ms)",
            "Duración (ms)",
            "Amplitud (°)",
            "Desviación (%)",
            "Velocidad Máxima (°/s)",
        ],
    )
    stats = _Stats(
        test=test_name,
    )

    saccade: Saccade
    for idx, saccade in enumerate(test.hor_saccades):
        ds.append(
            [
                idx + 1,
                saccade.onset,
                saccade.offset,
                saccade.latency,
                saccade.duration,
                saccade.amplitude,
                saccade.deviation,
                saccade.peak_velocity,
            ]
        )

        stats.add_sample(
            saccade.latency,
            saccade.duration,
            saccade.amplitude,
            saccade.deviation,
            saccade.peak_velocity,
        )

    return ds, stats


def _metadata_dataset(study: Study) -> Dataset:
    ds = Dataset(
        title="Estudio",
        headers=[
            "Campo",
            "Valor",
        ],
    )

    ds.append(["Fecha", study.recorded_at])
    ds.append(["Cantidad de Pruebas", len(study) - 2])
    ds.append(["Calibración Horizontal", study.hor_calibration])
    ds.append(["Calibración Horizontal Dif", study.hor_calibration_diff])

    return ds


def _stats_dataset(stats: list[_Stats]) -> Dataset:
    ds = Dataset(
        title="Estadísticas",
        headers=_Stats.headers(),
    )

    for stats in stats:
        ds.append(stats.row)

    return ds


def saccadic_report(study: Study, filepath: str):
    """Create a saccadic report.

    Args:
        study (Study): Study.
        filepath (str): Filepath.
    """
    tests_list = []
    stats_list = []

    for test in study:
        ds, stats = _test_dataset(test)
        tests_list.append(ds)
        stats_list.append(stats)

    study_ds = _metadata_dataset(study)

    workbook = Workbook()
    workbook.add_sheet(study_ds)
    workbook.add_sheet(_stats_dataset(stats_list))

    for test in tests_list:
        workbook.add_sheet(test)

    if not filepath.lower().endswith(".xlsx"):
        filepath += ".xlsx"

    with open(filepath, "wb") as f:
        f.write(workbook.export("xlsx"))
