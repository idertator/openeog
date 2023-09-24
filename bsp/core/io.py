from datetime import datetime
from io import BytesIO
from json import dumps, loads
from zipfile import ZipFile

from numpy import load, savez_compressed

from .models import Study, Test, TestType


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
                hor_stimuli=test.hor_stimuli,
                hor_channel=test.hor_channel,
                ver_stimuli=test.ver_stimuli,
                ver_channel=test.ver_channel,
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
                tests.append(
                    Test(
                        test_type=TestType(test["test_type"]),
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
            hor_calibration=manifest.get("hor_calibration", None),
            hor_calibration_diff=manifest.get("hor_calibration_diff", None),
            ver_calibration=manifest.get("ver_calibration", None),
            ver_calibration_diff=manifest.get("ver_calibration_diff", None),
        )
