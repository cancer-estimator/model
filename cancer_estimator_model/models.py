from typing import Tuple
from pathlib import Path
import os

from catboost import CatBoostRegressor
import matplotlib.pyplot as plt

import pandas

from cancer_estimator_model import datasets

_base_path = os.path.dirname(os.path.dirname(__file__))
_models_path = os.getenv("MODELS_DIR", os.path.join(_base_path, "models"))
models_dir = Path(_models_path)
model_path = models_dir / "model.cbm"


feature_selection = [
    "AGE",
    "SMOKING",  # float
    "YELLOW_FINGERS",  # float
    "ANXIETY",  # float
    "PEER_PRESSURE",  # float
    "CHRONIC_DISEASE",  # float
    "ALLERGY",  # float
    "WHEEZING",  # float
    "ALCOHOL_CONSUMING",  # float
    "FATIGUE",
    "COUGHING",
    "SHORTNESS_OF_BREATH",
    "SWALLOWING_DIFFICULTY",
    "CHEST_PAIN",
    "GENDER_FEMALE",
    "GENDER_MALE",
    "COLD_SYMPTOMNS",
    "RESPIRATORY_SYMPTOMNS",
    "SNORING",
    "AIR_POLLUTION",  # none
    "ALCOHOL_USE",  # none
    "DUST_ALLERGY",  # none
    "OCCUPATIONAL_HAZARDS",  # none
    "GENETIC_RISK",  # none
    "CHRONIC_LUNG_DISEASE",  # none
    "BALANCED_DIET",  # none
    "OBESITY",  # none
    "PASSIVE_SMOKER",  # none
    "COUGHING_OF_BLOOD",  # none
    "WEIGHT_LOSS",  # none
    "FREQUENT_COLD",  # none
    "DRY_COUGH",  # none
    "FEVER",  # none
    "PAINS",  # none
    "NASAL_CONGESTION",  # none
    "RUNNY_NOSE",  # none
    "DIARRHEA",  # none
]

cat_features = [
    # # NOTE: code to be used when proper propcessing
    # of missing is done
    #
    # x for x in feature_selection
    # if x not in ["AGE"]

    "FATIGUE",
    "COUGHING",
    "SHORTNESS_OF_BREATH",
    "SWALLOWING_DIFFICULTY",
    "CHEST_PAIN",
    "GENDER_FEMALE",
    "GENDER_MALE",
    "COLD_SYMPTOMNS",
    "RESPIRATORY_SYMPTOMNS",
    "SNORING",
]

target = "LUNG_CANCER_RISK"


def _get_train_dataset_treated() -> Tuple[pandas.DataFrame, pandas.DataFrame]:
    df = datasets.get_train_dataset()
    X = df[feature_selection]
    # cast cat features to integers
    # problem with missing values: from float columns there is nan
    # X[cat_features] = X[cat_features].astype(int)
    y = df[target].astype(int)
    return X, y


def _get_model():
    return CatBoostRegressor(
        iterations=500,
        depth=6,
        eval_metric="RMSE",
        learning_rate=0.1,
        cat_features=cat_features,
        verbose=100
    )


def train():
    print("[train] start training model")
    X, y = _get_train_dataset_treated()
    print("[train] samples: ", len(X))
    features = list(X.columns)
    print(f"[train] selected features(n={len(features)}): ", ", ".join(features))
    model = _get_model()
    model.fit(X, y)
    return model


def load() -> CatBoostRegressor:
    return CatBoostRegressor.load_model(model_path)


def save(model: CatBoostRegressor):
    model.save_model(model_path)
    save_feature_importance(model)


def save_feature_importance(model: CatBoostRegressor, n_features: int = 15):
    feature_importance = model.get_feature_importance(type='FeatureImportance')[:n_features]
    feature_names = model.feature_names_
    sorted_idx = feature_importance.argsort()[:n_features]

    plt.figure(figsize=(10, 5))
    plt.barh(range(len(sorted_idx)), feature_importance[sorted_idx], align='center')
    plt.yticks(range(len(sorted_idx)), [feature_names[i] for i in sorted_idx])
    plt.xlabel('Feature Importance')
    plt.title('CatBoost Feature Importance')
    plt.tight_layout()
    fpath = models_dir / "feature_importance.png"
    plt.savefig(fpath)
    print(f"[train] feature importance saved at: {fpath}")
