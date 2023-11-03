from pydantic import BaseModel
from dataclasses import dataclass
from pathlib import Path
import typing
from mlengine.common.utils import read_yaml
import os

CONFIG_FILE_PATH = Path("config/settings.yaml")


class Singleton(type):
    """
    https://stackoverflow.com/questions/6760685/creating-a-singleton-in-python
    """
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class SettingsManager(metaclass=Singleton):
    def __init__(self, config_filepath=CONFIG_FILE_PATH):
        pass
        self.settings = read_yaml(config_filepath)

    def initialize_settings(self, settings_class):
        return settings_class(**self.settings)


class Settings(BaseModel):
    x1: int


settings_manager = SettingsManager()
settings = settings_manager.initialize_settings(Settings)
