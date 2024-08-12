#!env python

from pathlib import Path

from tqdm import tqdm

from openeog.core.io import load_study, save_study
from openeog.core.models import Study

BASE_PATH = "/Users/idertator/Registros/july2024"
PURSUIT_PATH = Path(BASE_PATH) / "pursuits"

# TODO: Eliminar los que tengan error de calbración >= 50%

PURSUIT_STUDIES = [
    "Prueba_Persecucion_01.oeog",
    "Prueba_Persecucion_02.oeog",
    "Prueba_Persecucion_03.oeog",
    "Prueba_Persecucion_06.oeog",
    "Prueba_Persecucion_07.oeog",
    "Prueba_Persecucion_08.oeog",
    "Prueba_Persecucion_09.oeog",
    "Prueba_Persecucion_10.oeog",
    "Prueba_Persecucion_11.oeog",
    "Prueba_Persecucion_12.oeog",
    "Prueba_Persecucion_13.oeog",
    "Prueba_Persecucion_14.oeog",
    "Prueba_Persecucion_15.oeog",
    "Prueba_Persecucion_18.oeog",
    "Prueba_Persecucion_19.oeog",
    "Prueba_Persecucion_20.oeog",
    "Prueba_Persecucion_21.oeog",
    "Prueba_Persecucion_22.oeog",
    "Prueba_Persecucion_24.oeog",
    "Prueba_Persecucion_25.oeog",
    "Prueba_Persecucion_26.oeog",
    "Prueba_Persecucion_27.oeog",
    "Prueba_Persecucion_29.oeog",
    "Prueba_Persecucion_30.oeog",
    "Prueba_Persecucion_31.oeog",
    "Prueba_Persecucion_32.oeog",
    "Prueba_Persecucion_33.oeog",
    "Prueba_Persecucion_34.oeog",
    "Prueba_Persecucion_35.oeog",
]

OUTPUT_PATH = "pursuits_biomarkers.xlsx"


def process_study(study: Study, pursuit: bool = False):
    pass


if __name__ == "__main__":
    PURSUIT_OUTPUT_PATH = PURSUIT_PATH / OUTPUT_PATH
    if not PURSUIT_OUTPUT_PATH.exists():
        PURSUIT_OUTPUT_PATH.mkdir(parents=True)

    for filename in tqdm(
        PURSUIT_STUDIES,
        desc="Processing pursuit studies",
    ):
        print(f"Processing study {filename}")
        fullpath = PURSUIT_PATH / filename
        if fullpath.exists():
            study = load_study(fullpath)
            process_study(study, pursuit=True)

            output_path = PURSUIT_OUTPUT_PATH / filename
            save_study(study, output_path)

        print()
