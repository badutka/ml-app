import os
import yaml
from box import ConfigBox
from box.exceptions import BoxValueError
from ensure import ensure_annotations
from pathlib import Path
from functools import reduce

from mlengine.common.logger import logger


@ensure_annotations
def read_yaml(path_to_yaml: Path) -> ConfigBox:
    """
    Reads yaml file and returns ConfigBox.

    :param path_to_yaml: Path to the yaml file.
    :raises ValueError: if yaml file is empty.
    :returns ConfigBox: returns object with nested properties instead of a dictionary.
    """
    try:
        with open(path_to_yaml) as yaml_file:
            content = yaml.safe_load(yaml_file)
            logger.info(f"Settings file [{path_to_yaml}] loaded successfully.\n{30 * '*'}")
            return ConfigBox(content)
    except BoxValueError:
        raise ValueError(f"Settings file [{path_to_yaml}] is empty.")
    except Exception as e:
        raise e


@ensure_annotations
def create_directories(path_to_directories: list, verbose: bool = True):
    """
    Creates directories from a list.

    :param path_to_directories: list of path of directories.
    :param verbose: boolean indicating whether to log information about successful directory setup or not.
    # :param ignore_log: (bool) ignore if multiple dirs is to be created. Defaults to False.
    """
    for path in path_to_directories:
        os.makedirs(path, exist_ok=True)
        if verbose:
            logger.info(f"created directory at: {path}")


@ensure_annotations
def get_size(path: Path) -> str:
    """
    Returns size of file in KB.

    :param path: Path of the file.
    :returns str: description of size in KB.
    """
    size_in_kb = round(os.path.getsize(path) / 1024)
    return f"~ {size_in_kb} KB"


def get_num_fits(grid: dict, cv: int) -> int:
    """
    Returns number of all total fits (number of folds times number of all combinations of hyper-parameters) for a GridSearch
    :param grid: hyper-parameter dictionary for a given model.
    :param cv: number of folds used in cross validation.
    :return: int, number of total fits .
    """
    num_cand = [len(params) if params else 1 for params in grid.values()]
    return cv * (reduce(lambda x, y: x * y, num_cand) if grid else 1)


def setup_param_grid(models_params: dict, name: str) -> dict:
    """
    Returns hyper-parameter grid for a given model with parameter names adjusted for model name (model-name__param_name).
    If a certain model is not present in the yaml file, then returns empty dictionary.

    :param models_params: hyper-parameter grid for all models included in yaml file
    :param name: name of the model
    :return: dict,
    """
    if name not in models_params:
        return {}

    model_params = models_params[name]
    param_grid = get_param_grid(model_params)
    param_grid = make_pipeline_grid_names(name, param_grid)

    return param_grid


def get_param_grid(model_params: dict) -> dict:
    """
    Returns a dictionary of hyperparameters for a given model name.
    Parameters are first picked from under random_search key, then from grid_search.
    If both are empty, then defaults to empty dict

    :param model_params: dict obtained from reading yaml file
    :return: dict, params for a given model name
    """
    match model_params:
        case {'random_search': d} if d:
            return model_params['random_search']
        case {'grid_search': d} if d:
            return model_params['grid_search']
        case other:
            return {}


def make_pipeline_grid_names(name: str, param_grid: dict) -> dict:
    """
    Returns hyper-parameter grid for a given model with names adjusted for pipelines (in a format 'pipeline-name__param-name')

    :param name: name of the model.
    :param param_grid: dict - hyper-parameter grid for a given model name
    :return: new param grid with adjusted names
    """
    new_param_grid = {}
    for param_name, param_value in param_grid.items():
        new_param_grid[name + "__" + param_name] = param_value
    return new_param_grid
