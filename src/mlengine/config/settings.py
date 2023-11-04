from pydantic import BaseModel
from dataclasses import dataclass
from pathlib import Path
import typing
from mlengine.common.utils import read_yaml
import os
from box import ConfigBox


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
    def __init__(self):
        pass
        current_file_path = os.path.abspath(__file__)
        file_path = Path(os.path.join(os.path.dirname(current_file_path), "settings.yaml"))
        self.settings = read_yaml(file_path)

    # def get_settings(self) -> ConfigBox:
    #     return self.settings

    def initialize_settings(self, settings_class) -> ConfigBox:
        return settings_class(**self.settings)


class DataIngestionSettings(BaseModel):
    root_dir: str
    source_URL: str
    local_data_file: str
    unzip_dir: str


class Settings(BaseModel):
    artifacts_root: str
    data_ingestion: DataIngestionSettings


# settings = SettingsManager().get_settings()
settings = SettingsManager().initialize_settings(Settings)
