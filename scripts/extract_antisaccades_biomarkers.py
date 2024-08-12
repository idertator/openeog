#!env python

from pathlib import Path

from tqdm import tqdm

from openeog.core.io import load_study, save_study
from openeog.core.models import Study

BASE_PATH = "/Users/idertator/Registros/july2024"
ANTISACCADIC_PATH = Path(BASE_PATH) / "antisaccades"


# TODO: Eliminar los que tengan error de calbración >= 50%

ANTISACCADIC_STUDIES = [
    "Prueba_Antisacadica_01.oeog",
    "Prueba_Antisacadica_02.oeog",
    "Prueba_Antisacadica_04.oeog",
    "Prueba_Antisacadica_05.oeog",
    "Prueba_Antisacadica_06.oeog",  # He añadido esta prueba porque es de un sujeto de 98 interesante de estudiar
    "Prueba_Antisacadica_07.oeog",
    "Prueba_Antisacadica_08.oeog",
    "Prueba_Antisacadica_09.oeog",
    "Prueba_Antisacadica_10.oeog",
    "Prueba_Antisacadica_11.oeog",
    "Prueba_Antisacadica_12.oeog",
    "Prueba_Antisacadica_13.oeog",
    "Prueba_Antisacadica_14.oeog",
    "Prueba_Antisacadica_15.oeog",
    "Prueba_Antisacadica_16.oeog",
    "Prueba_Antisacadica_17.oeog",
    "Prueba_Antisacadica_18.oeog",
    "Prueba_Antisacadica_20.oeog",
    "Prueba_Antisacadica_21.oeog",
    "Prueba_Antisacadica_22.oeog",
    "Prueba_Antisacadica_27.oeog",
    "Prueba_Antisacadica_30.oeog",
    "Prueba_Antisacadica_33.oeog",
    "Prueba_Antisacadica_34.oeog",
    "Prueba_Antisacadica_35.oeog",
]

OUTPUT_PATH = "antisaccades_biomarkers.xlsx"


def process_study(study: Study, pursuit: bool = False):
    pass


if __name__ == "__main__":
    ANTISACCADIC_OUTPUT_PATH = ANTISACCADIC_PATH / OUTPUT_PATH
    if not ANTISACCADIC_OUTPUT_PATH.exists():
        ANTISACCADIC_OUTPUT_PATH.mkdir(parents=True)

    for filename in tqdm(
        ANTISACCADIC_STUDIES,
        desc="Processing antisaccadic studies",
    ):
        print(f"Processing study {filename}")
        fullpath = ANTISACCADIC_PATH / filename
        if fullpath.exists():
            study = load_study(fullpath)
            process_study(study)

            output_path = ANTISACCADIC_OUTPUT_PATH / filename
            save_study(study, output_path)

        print()
