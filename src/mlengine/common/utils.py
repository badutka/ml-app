import os
import yaml
from box import ConfigBox
from box.exceptions import BoxValueError
from ensure import ensure_annotations
from pathlib import Path

from mlengine.common.logger import logger


@ensure_annotations
def read_yaml(path_to_yaml: Path) -> ConfigBox:
    """reads yaml file and returns ConfigBox

    Args:
        path_to_yaml (str): Path to the yaml file

    Raises:
        ValueError: if yaml file is empty
        e: empty file

    Returns:
        ConfigBox: returns object with nested properties instead of a dictionary
    """
    try:
        with open(path_to_yaml) as yaml_file:
            content = yaml.safe_load(yaml_file)
            logger.info(f"Settings file [{path_to_yaml}] loaded successfully.")
            return ConfigBox(content)
    except BoxValueError:
        raise ValueError(f"Settings file [{path_to_yaml}] is empty.")
    except Exception as e:
        raise e
