from pydantic import BaseModel, Field
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


@dataclass(frozen=True)
class DataIngestionSettings(BaseModel):
    root_dir: Path
    source_URL: str
    local_data_file: Path
    unzip_dir: Path


@dataclass(frozen=True)
class DataValidationSettings(BaseModel):
    data_file: Path
    root_dir: Path
    status_file: Path


@dataclass(frozen=True)
class PlotLayoutsSettings(BaseModel):
    features_plots_layout: typing.Dict = Field(default_factory=dict)

    def __init__(self, **data):
        if 'features_plots_layout' in data and isinstance(data['features_plots_layout'], ConfigBox):
            data['features_plots_layout'] = dict(data['features_plots_layout'])
        super().__init__(**data)


@dataclass(frozen=True)
class Settings(BaseModel):
    artifacts_root: Path
    data_ingestion: DataIngestionSettings
    data_validation: DataValidationSettings
    plot_layouts: PlotLayoutsSettings


class SettingsManager(metaclass=Singleton):
    def __init__(self):
        pass
        current_file_path = os.path.abspath(__file__)
        file_path = Path(os.path.join(os.path.dirname(current_file_path), "settings.yaml"))
        self.settings = read_yaml(file_path)

    # def get_settings(self) -> ConfigBox:
    #     return self.settings

    def initialize_settings(self) -> Settings:
        return Settings(**self.settings)


# settings = SettingsManager().get_settings()
settings = SettingsManager().initialize_settings()
