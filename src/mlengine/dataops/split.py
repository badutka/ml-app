from box import ConfigBox
import os
from pathlib import Path

from mlengine.common.logger import logger
from mlengine.data_read.read import read_csv_file
from sklearn.model_selection import train_test_split


class DataSplitter():
    def __init__(self, config: ConfigBox):
        self.config: ConfigBox = config
        self.target = self.config.model.target
        self.data_file_path = self.config.data_transformation.root_dir
        self.data_file_name = self.config.data_transformation.data_file_tnsf
        self.data_file: Path = Path(os.path.join(self.data_file_path, self.data_file_name))
        self.root_dir: Path = self.config.data_split.root_dir
        self.split_files: list = self.config.data_split.split_files

    def train_validate_test_split(self):
        try:
            df = read_csv_file(self.data_file)
            X, y = self.get_X_y(df, self.target)
            X_train, X_validate, X_test, y_train, y_validate, y_test = self.get_train_validate_test_X_y(X, y)
            self.save_split_data([X_train, X_validate, X_test, y_train, y_validate, y_test])
            logger.info(f'Successfully split data into: {self.split_files}')
        except Exception as e:
            raise e

    def get_X_y(self, df, target):
        y = df[target]
        X = df.drop(target, axis=1)
        return X, y

    def get_train_validate_test_X_y(self, X, y, test_size=0.4, *args, **kwargs):
        X_train, X_test, y_train, y_test = train_test_split(X, y, stratify=None, test_size=test_size, *args, **kwargs)
        X_validate, X_test, y_validate, y_test = train_test_split(X_test, y_test, stratify=None, test_size=0.5, *args, **kwargs)
        return X_train, X_validate, X_test, y_train, y_validate, y_test

    def save_split_data(self, split_data):
        for i, data in enumerate(split_data):
            data.to_csv(os.path.join(self.root_dir, self.split_files[i]))
