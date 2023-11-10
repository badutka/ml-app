import sys
import pandas as pd
import os
import joblib

from mlengine.common.exceptions import MissingCriticalFileException
from mlengine.config.settings import settings
from dataclasses import dataclass, asdict


class Prediction:
    def __init__(self):
        pass

    def predict(self, features):
        preprocessor_path = os.path.join(settings.model_preprocessing.root_dir, settings.model_preprocessing.prep_pipeline_file)
        model_path = os.path.join(settings.model_testing.root_dir, "model.pkl")

        try:
            model = joblib.load(model_path)
            preprocessor = joblib.load(preprocessor_path)
        except Exception as e:
            raise MissingCriticalFileException('PRD_EX_001', 'Model file or preprocessor file missing.')  # todo: move to utils

        data_scaled = preprocessor.transform(features)

        return model.predict(data_scaled)


@dataclass
class CustomData:
    gender: str
    race_ethnicity: str
    parental_level_of_education: str
    lunch: str
    test_preparation_course: str
    reading_score: int
    writing_score: int

    def get_data_as_data_frame(self):
        data_dict = {k: str(v) for k, v in asdict(self).items()}
        return pd.DataFrame([data_dict])  # wrapping dictionary into a list to avoid having to pass index
