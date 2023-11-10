from box import ConfigBox
import os
from pathlib import Path
import joblib

from sklearn.ensemble import RandomForestRegressor, AdaBoostRegressor
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor
from catboost import CatBoostRegressor
from xgboost import XGBRegressor

from sklearn.pipeline import Pipeline
from sklearn.model_selection import RandomizedSearchCV, GridSearchCV

from mlengine.common.logger import logger
from mlengine.data_read.read import read_csv_file
from mlengine.common.utils import get_num_fits, setup_param_grid, read_yaml


class ModelTrainer():
    def __init__(self, config: ConfigBox):
        self.config: ConfigBox = config
        self.X_train_file: Path = self.config.req_files[0]
        self.y_train_file: Path = self.config.req_files[1]
        self.preprocessing_pipeline_path: Path = self.config.req_files[2]
        self.X_train = None
        self.y_train = None
        self.models = {
            "LinearRegression": LinearRegression(),
            "Lasso": Lasso(),
            "Ridge": Ridge(),
            "K-NeighborsRegressor": KNeighborsRegressor(),
            "DecisionTreeRegressor": DecisionTreeRegressor(),
            "RandomForestRegressor": RandomForestRegressor(),
            "XGBRegressor": XGBRegressor(),
            "CatBoostingRegressor": CatBoostRegressor(verbose=False),
            "AdaBoostRegressor": AdaBoostRegressor()
        }
        self.models_params = read_yaml(Path('src/mlengine/config/params.yaml'))

        self.fit_best_models = []

    def get_training_data(self):
        self.X_train = read_csv_file(self.X_train_file)
        self.y_train = read_csv_file(self.y_train_file).squeeze()

    def preprocess_training_data(self):
        preprocessing_pipeline = joblib.load(self.preprocessing_pipeline_path)
        self.X_train = preprocessing_pipeline.transform(self.X_train)

    def train_models(self):
        model_pipelines = {name: Pipeline(steps=[(name, clf)]) for name, clf in self.models.items()}

        for name, model_pipeline in model_pipelines.items():
            logger.info(f"Training {name} model...")

            param_grid = setup_param_grid(self.models_params, name)
            models = GridSearchCV(model_pipeline, param_grid=param_grid, cv=self.models_params[name].cv, verbose=False)
            best_model = models.fit(self.X_train, self.y_train).best_estimator_
            best_model.fit(self.X_train, self.y_train)  # retrain the model again on full training data (previously we were 1 fold short for each iter of CV)

            joblib.dump(best_model, os.path.join(self.config.models_dir, name + ".pkl"))

            logger.info(f"Training successful, model saved under '{name}.pkl'.")
