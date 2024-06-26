from typing import Dict
from pathlib import Path
import os

import pandas

from cancer_estimator_model import io

_base_path = os.getcwd() if not io.is_notebook() else os.path.dirname(os.path.dirname(__file__))
_datasets_path = os.getenv("DATASETS_DIR", os.path.join(_base_path, "datasets"))
datasets_dir = Path(_datasets_path)


def get_breast_cancer_datasets() -> Dict[str, pandas.DataFrame]:
    datasets_path = {
        "death": datasets_dir / "breast-cancer/death.xlsx",
        "recovered": datasets_dir / "breast-cancer/recovered.xlsx",
        "under_treatment": datasets_dir / "breast-cancer/under_treatment.xlsx",
    }
    assert [dataset.exists() for dataset in datasets_path.values()], "datasets not found, check dvc"
    return {key: pandas.read_excel(fpath)
            for key, fpath in datasets_path.items()}


def get_lung_cancer_survey_lung_cancer() -> pandas.DataFrame:
    return pandas.read_csv(datasets_dir / "lung-cancer/survey_lung_cancer.csv")


def get_lung_cancer_cancer_patient_data_sets() -> pandas.DataFrame:
    return pandas.read_csv(datasets_dir / "lung-cancer/cancer_patient_data_sets.csv")


def get_covid_dataset() -> pandas.DataFrame:
    return pandas.read_csv(datasets_dir / "lung-cancer/covid_dataset.csv", low_memory=False)


def get_integrated_dataset() -> pandas.DataFrame:
    return pandas.read_csv(datasets_dir / "lung-cancer/dataset_integrated.csv", low_memory=False)


def get_train_dataset() -> pandas.DataFrame:
    df = get_integrated_dataset()
    return df[df.SOURCE != 3]
