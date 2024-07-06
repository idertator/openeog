from datetime import datetime
from io import BytesIO
from json import dumps, loads
from zipfile import ZipFile

from numpy import load, savez_compressed

from .models import Conditions, Device, Hardware, Protocol, Study, Test, TestType


def save_study(study: Study, filepath: str):
    """Save a study to a file

    Args:
        study (Study): Study
        filepath (str): Filepath
    """
    with ZipFile(filepath, "w") as zip_file:
        zip_file.writestr("manifest.json", dumps(study.json, indent=4))

        test: Test
        for idx, test in enumerate(study):
            buff = BytesIO()
            savez_compressed(
                buff,
                hor_stimuli=test.hor_stimuli_raw,
                hor_channel=test.hor_channel_raw,
                ver_stimuli=test.ver_stimuli_raw,
                ver_channel=test.ver_channel_raw,
            )
            zip_file.writestr(f"test{idx:02}.npz", buff.getvalue())


def load_study(filepath: str) -> Study:
    """Load a study from a file

    Args:
        filepath (str): Filepath

    Returns:
        Study: Study
    """
    with ZipFile(filepath, "r") as zip_file:
        manifest = loads(zip_file.read("manifest.json"))

        if hardware_manifest := manifest.get("hardware"):
            hardware = Hardware(
                acquisition_device=Device(hardware_manifest["acquisition_device"]),
                acquisition_sampling_rate=hardware_manifest.get(
                    "acquisition_sampling_rate",
                    1000,
                ),
                stimuli_monitor=hardware_manifest["stimuli_monitor"],
                stimuli_monitor_refresh_rate=hardware_manifest.get(
                    "stimuli_monitor_refresh_rate",
                    None,
                ),
                stimuli_monitor_width=hardware_manifest["stimuli_monitor_width"],
                stimuli_monitor_height=hardware_manifest["stimuli_monitor_height"],
                stimuli_monitor_resolution_width=hardware_manifest[
                    "stimuli_monitor_resolution_width"
                ],
                stimuli_monitor_resolution_height=hardware_manifest[
                    "stimuli_monitor_resolution_height"
                ],
                stimuli_ball_radius=hardware_manifest["stimuli_ball_radius"],
            )
        else:
            hardware = None

        if conditions_manifest := manifest.get("conditions"):
            conditions = Conditions(
                light_intensity=conditions_manifest["light_intensity"],
                errors=conditions_manifest.get("errors", 0),
            )
        else:
            conditions = None

        tests = []
        for idx, test in enumerate(manifest["tests"]):
            with zip_file.open(f"test{idx:02}.npz") as buff:
                channels = load(buff)

                test_type = test["test_type"]

                # Small bug currection - Remove in future versions
                if test_type == "HorizontalSaccadicTest":
                    test_type = TestType.HorizontalSaccadic.value

                tests.append(
                    Test(
                        test_type=TestType(test_type),
                        angle=test["angle"],
                        hor_stimuli=channels["hor_stimuli"],
                        hor_channel=channels["hor_channel"],
                        ver_stimuli=channels["ver_stimuli"],
                        ver_channel=channels["ver_channel"],
                    )
                )

        return Study(
            recorded_at=datetime.fromtimestamp(manifest["recorded_at"]),
            protocol=Protocol(test.get("protocol", "saccadic")),
            hardware=hardware,
            conditions=conditions,
            tests=tests,
            hor_calibration=float(manifest.get("hor_calibration", None) or 1.0),
            hor_calibration_diff=float(
                manifest.get("hor_calibration_diff", None) or 1.0
            ),
            ver_calibration=float(manifest.get("ver_calibration", None) or 1.0),
            ver_calibration_diff=float(
                manifest.get("ver_calibration_diff", None) or 1.0
            ),
        )
