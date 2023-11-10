from box import ConfigBox
from pathlib import Path
import os
import joblib

from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.feature_selection import RFE
from sklearn.svm import SVR
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer

from mlengine.data_read.read import read_csv_file


class Preprocessor():
    def __init__(self, config: ConfigBox):
        self.config: ConfigBox = config
        self.X_train_file: Path = self.config.req_files[0]
        self.y_train_file: Path = self.config.req_files[1]

        self.X_train = None
        self.y_train = None
        self.prep_pipeline = None

        self.pipeline_file: Path = Path(os.path.join(self.config.root_dir, self.config.prep_pipeline_file))

    def get_features_data(self):
        self.X_train = read_csv_file(self.X_train_file)
        self.y_train = read_csv_file(self.y_train_file).squeeze()

    def setup_preprocessing_pipeline(self):
        num_features = self.X_train.select_dtypes(exclude="object").columns
        cat_features = self.X_train.select_dtypes(include="object").columns

        num_pipeline = Pipeline(steps=[
            ("SimpleImputer", SimpleImputer(strategy='mean')),
            ("StandardScaler", StandardScaler())
        ])

        cat_pipeline = Pipeline(steps=[
            ("SimpleImputer", SimpleImputer(strategy='most_frequent')),
            ("OneHotEncoder", OneHotEncoder())
        ])

        preprocessor = ColumnTransformer(
            [
                ("NumericalPipeline", num_pipeline, num_features),
                ("CategoricalPipeline", cat_pipeline, cat_features),
            ]
        )

        rfe = RFE(SVR(kernel="linear"), step=1)

        self.prep_pipeline = Pipeline(steps=[('preprocessor', preprocessor), ('rfe', rfe)])

    def fit_train_data(self):
        self.prep_pipeline.fit(self.X_train, self.y_train)

    def save_preprocessing_pipeline(self):
        joblib.dump(self.prep_pipeline, self.pipeline_file)
