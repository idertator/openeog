from datetime import datetime
from io import BytesIO
from json import dumps, loads
from zipfile import ZipFile

from numpy import load, savez_compressed

from .models import Protocol, Study, Test, TestType


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

        tests = []
        for idx, test in enumerate(manifest["tests"]):
            with zip_file.open(f"test{idx:02}.npz") as buff:
                channels = load(buff)

                print(channels.keys())

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
            tests=tests,
            hor_calibration=float(manifest.get("hor_calibration", None) or 1.0),
            hor_calibration_diff=float(
                manifest.get("hor_calibration_diff", None) or 1.0
            ),
            ver_calibration=float(manifest.get("ver_calibration", None) or 1.0),
            ver_calibration_diff=float(
                manifest.get("ver_calibration_diff", None) or 1.0
            ),
            protocol=Protocol(test.get("protocol", "saccadic")),
        )
