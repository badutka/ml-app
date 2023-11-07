import numpy as np
import os
from box import ConfigBox
from pathlib import Path
import joblib
import json

from sklearn.svm import SVR
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error

from mlengine.common.exceptions import MissingCriticalFileException
from mlengine.data_read.read import read_csv_file


class ModelEvaluator():
    def __init__(self, config: ConfigBox):
        self.config: ConfigBox = config
        self.X_file: Path = self.config.req_files[0]
        self.y_file: Path = self.config.req_files[1]
        self.preprocessing_pipeline_path: Path = self.config.req_files[2]
        self.models = None
        self.X = None
        self.y = None

    def load_models(self):
        model_files = os.listdir(self.config.models_dir)
        if not model_files:
            raise MissingCriticalFileException('VLD_EX_002', 'No models to load from directory. Make sure the directory is correct and previous pipelines work without any issues.')
        self.models = {Path(model_file).stem: joblib.load(os.path.join(self.config.models_dir, model_file)) for model_file in model_files}

    def load_data_files(self):
        self.X = read_csv_file(self.X_file)
        self.y = read_csv_file(self.y_file).squeeze()

    def preprocess_data(self):
        preprocessing_pipeline = joblib.load(self.preprocessing_pipeline_path)
        self.X = preprocessing_pipeline.transform(self.X)

    def evaluate_regression_model(self, y_true, y_pred):
        mae = mean_absolute_error(y_true, y_pred)
        mse = mean_squared_error(y_true, y_pred)
        rmse = np.sqrt(mse)
        r2_square = r2_score(y_true, y_pred)
        return mae, rmse, r2_square

    def save_regression_evaluation(self):
        all_metrics = {}

        for name, model in self.models.items():
            y_pred = model.predict(self.X)
            mae, rmse, r2 = self.evaluate_regression_model(self.y, y_pred)
            model_metrics = {"RMSE": rmse, "MAE": mae, "R2": r2}
            all_metrics[name] = model_metrics

        output_file = "model_metrics.json"

        with open(os.path.join(self.config.root_dir, output_file), "w") as file:
            json.dump(all_metrics, file, indent=4)
