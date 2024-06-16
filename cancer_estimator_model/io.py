import pandas


def dict_to_pandas(features: dict) -> pandas.DataFrame:
    features_uppercase = {k.upper(): v for k, v in features.items()}
    return pandas.json_normalize(features_uppercase)
