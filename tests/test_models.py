import pytest

from cancer_estimator_model import io, models


def test_generate_artificial_variables_successful():
    row = {
        "FATIGUE": 1,
        "SHORTNESS_OF_BREATH": 1,
        "SWALLOWING_DIFFICULTY": 1,
        "WHEEZING": 1,
        "DRY_COUGH": 1,
        "COUGHING_OF_BLOOD": 1,
        "FREQUENT_COLD": 1,
        "GENDER": "Male",
        "ALCOHOL_USE": 1,
        "CHRONIC_LUNG_DISEASE": 1,
    }
    df = io.dict_to_pandas(row)
    expected = {
        "COLD_SYMPTOMNS": 4,
        "RESPIRATORY_SYMPTOMNS": 5,
        "GENDER_FEMALE": 0,
        "GENDER_MALE": 1,
        "ALCOHOL_CONSUMING": 1,
        "CHRONIC_DISEASE": 1
    }
    df_with_artificial_variables = models.generate_artificial_variables(df)[models.artificial_variables]
    artificial_variables = df_with_artificial_variables.to_dict(orient="records")[0]
    assert artificial_variables == expected
