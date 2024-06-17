import pandas


def dict_to_pandas(features: dict) -> pandas.DataFrame:
    features_uppercase = {k.upper(): v for k, v in features.items()}
    return pandas.json_normalize(features_uppercase)


def is_notebook() -> bool:
    # ref: https://stackoverflow.com/a/39662359/3749971
    try:
        shell = get_ipython().__class__.__name__  # type: ignore
        if shell == 'ZMQInteractiveShell':
            return True   # Jupyter notebook or qtconsole
        elif shell == 'TerminalInteractiveShell':
            return False  # Terminal running IPython
        else:
            return False  # Other type (?)
    except NameError:
        return False      # Probably standard Python interpreter
