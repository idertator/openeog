from datetime import datetime
from io import BytesIO
from json import dumps, loads
from zipfile import ZipFile

from numpy import load, savez_compressed

from .models import Study, Test, TestType


def save_study(study: Study, filepath: str):
    with ZipFile(filepath, "w") as zip_file:
        zip_file.writestr("manifest.json", dumps(study.json, indent=4))

        test: Test
        for idx, test in enumerate(study):
            buff = BytesIO()
            savez_compressed(
                buff,
                horizontal_stimuli=test.horizontal_stimuli,
                horizontal_channel=test.horizontal_channel,
                vertical_stimuli=test.vertical_stimuli,
                vertical_channel=test.vertical_channel,
            )
            zip_file.writestr(f"test{idx:02}.npz", buff.getvalue())


def load_study(filepath: str) -> Study:
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
                        horizontal_stimuli=channels["horizontal_stimuli"],
                        horizontal_channel=channels["horizontal_channel"],
                        vertical_stimuli=channels["vertical_stimuli"],
                        vertical_channel=channels["vertical_channel"],
                    )
                )

        return Study(
            recorded_at=datetime.fromtimestamp(manifest["recorded_at"]),
            *tests,
        )
