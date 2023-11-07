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


class ModelTrainer():
    def __init__(self, config: ConfigBox):
        self.config: ConfigBox = config
        self.X_train_file: Path = self.config.req_files[0]
        self.y_train_file: Path = self.config.req_files[1]
        self.preprocessing_pipeline_path: Path = self.config.req_files[2]
        self.X_train = None
        self.y_train = None
        self.models = {
            "Linear Regression": LinearRegression(),
            "Lasso": Lasso(),
            "Ridge": Ridge(),
            "K-Neighbors Regressor": KNeighborsRegressor(),
            "Decision Tree": DecisionTreeRegressor(),
            "Random Forest Regressor": RandomForestRegressor(),
            "XGBRegressor": XGBRegressor(),
            "CatBoosting Regressor": CatBoostRegressor(verbose=False),
            "AdaBoost Regressor": AdaBoostRegressor()
        }

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
            models = GridSearchCV(model_pipeline, param_grid={}, cv=5, verbose=True)
            best_model = models.fit(self.X_train, self.y_train).best_estimator_
            best_model.fit(self.X_train, self.y_train)  # retrain the model again on full training data (previously we were 1 fold short for each iter of CV)

            joblib.dump(best_model, os.path.join(self.config.models_dir, name + ".pkl"))
