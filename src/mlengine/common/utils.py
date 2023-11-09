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
    returns size in KB

    :param path: Path of the file
    :returns str: size in KB
    """
    size_in_kb = round(os.path.getsize(path) / 1024)
    return f"~ {size_in_kb} KB"


def get_num_fits(grid, cv):
    num_cand = [len(params) if params else 1 for params in grid.values()]
    return cv * (reduce(lambda x, y: x * y, num_cand) if grid else 1)
