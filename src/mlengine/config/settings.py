import pydantic
from pydantic import BaseModel, Field, model_validator, ConfigDict, constr
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


class UnexpectedPropertyValidator(BaseModel):
    class Config:
        frozen = True
        protected_namespaces = ()

    @model_validator(mode='before')
    def check_unexpected_properties(cls, values):
        expected_properties = set(cls.__annotations__.keys())
        unexpected_properties = set(values) - expected_properties
        if unexpected_properties:
            raise ValueError(f"Unexpected properties: {', '.join(unexpected_properties)}")
        return values


class DataIngestionSettings(UnexpectedPropertyValidator):
    root_dir: Path
    source_URL: str
    zipped_file: str
    unzip_dir: Path
    data_file: str


class DataValidationSettings(UnexpectedPropertyValidator):
    root_dir: Path
    req_files: typing.List
    status_file: str


class DataTransformationSettings(UnexpectedPropertyValidator):
    root_dir: Path
    req_files: typing.List
    data_file_tnsf: str
    status_file: str


class DataValidationPostTransformSettings(UnexpectedPropertyValidator):
    root_dir: Path
    req_files: typing.List
    status_file: str


class DataSplitSettings(UnexpectedPropertyValidator):
    test_size: pydantic.StrictFloat
    root_dir: Path
    req_files: typing.List
    split_files: typing.List
    status_file: str


class ModelSettings(UnexpectedPropertyValidator):
    target: pydantic.StrictStr
    model_type: constr(pattern='^(regression|classification)$')
    preprocessing: constr(pattern='^(joint|disjoint)$')


class ModelPreprocessingSettings(UnexpectedPropertyValidator):
    root_dir: Path
    req_files: typing.List
    prep_pipeline_file: str
    status_file: Path


class ModelTrainingSettings(UnexpectedPropertyValidator):
    root_dir: Path
    req_files: typing.List
    status_file: Path


class PlotLayoutsSettings(UnexpectedPropertyValidator):
    features_plots_layout: typing.Dict = Field(default_factory=dict)


class Settings(UnexpectedPropertyValidator):
    artifacts_root: Path

    data_ingestion: DataIngestionSettings
    data_validation: DataValidationSettings
    data_transformation: DataTransformationSettings
    data_validation_post_t: DataValidationPostTransformSettings
    data_split: DataSplitSettings

    model: ModelSettings
    model_preprocessing: ModelPreprocessingSettings
    model_training: ModelTrainingSettings

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
        # print(model_config['protected_namespaces'])
        return Settings(**self.settings)


# settings = SettingsManager().get_settings()
settings = SettingsManager().initialize_settings()
