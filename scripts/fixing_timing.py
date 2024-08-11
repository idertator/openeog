#!env python

from pathlib import Path
from openeog.core.logging import log
from openeog.core.io import load_study, save_study
from openeog.core.models import Study, Test
from openeog.core.denoising import denoise_35
from tqdm import tqdm

BASE_PATH = "/Users/idertator/Registros/july2024"
ANTISACCADIC_PATH = Path(BASE_PATH) / "antisaccades"
PURSUIT_PATH = Path(BASE_PATH) / "pursuits"

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

OUTPUT_PATH = "processed_timing_fixed"


def process_study(study: Study):
    test: Test
    for index, test in enumerate(study):
        log.debug(f"Procesando test {index} / {len(study) - 1}")

        # Fixing timing
        if index == 0:
            hor_channel_cutted = test._hor_channel[222:]
            hor_stimuli_cutted = test._hor_stimuli[:-222]
            ver_channel_cutted = test._ver_channel[222:]
            ver_stimuli_cutted = test._ver_stimuli[:-222]
        else:
            hor_channel_cutted = test._hor_channel[194:]
            hor_stimuli_cutted = test._hor_stimuli[:-194]
            ver_channel_cutted = test._ver_channel[194:]
            ver_stimuli_cutted = test._ver_stimuli[:-194]

        # Denoising
        hor_channel_processed = denoise_35(hor_channel_cutted)
        test._hor_channel = hor_channel_processed
        test._hor_stimuli = hor_stimuli_cutted

        ver_channel_processed = denoise_35(ver_channel_cutted)
        test._ver_channel = ver_channel_processed
        test._ver_stimuli = ver_stimuli_cutted


if __name__ == "__main__":
    ANTISACCADIC_OUTPUT_PATH = ANTISACCADIC_PATH / OUTPUT_PATH
    if not ANTISACCADIC_OUTPUT_PATH.exists():
        ANTISACCADIC_OUTPUT_PATH.mkdir(parents=True)

    for filename in tqdm(
        ANTISACCADIC_STUDIES,
        desc="Processing antisaccadic studies",
    ):
        fullpath = ANTISACCADIC_PATH / filename
        if fullpath.exists():
            study = load_study(fullpath)
            process_study(study)

            output_path = ANTISACCADIC_OUTPUT_PATH / filename
            save_study(study, output_path)

    PURSUIT_OUTPUT_PATH = PURSUIT_PATH / OUTPUT_PATH
    if not PURSUIT_OUTPUT_PATH.exists():
        PURSUIT_OUTPUT_PATH.mkdir(parents=True)

    for filename in tqdm(
        PURSUIT_STUDIES,
        desc="Processing pursuit studies",
    ):
        fullpath = PURSUIT_PATH / filename
        if fullpath.exists():
            study = load_study(fullpath)
            process_study(study)

            output_path = PURSUIT_OUTPUT_PATH / filename
            save_study(study, output_path)
