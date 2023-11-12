import os
from box import ConfigBox
from pathlib import Path
import joblib
import json


class ModelPicker():
    def __init__(self, config: ConfigBox):
        self.config: ConfigBox = config
        self.test_metrics_file = Path(os.path.join(self.config.model_testing.root_dir, self.config.model_testing.metrics_file))
        self.selected_metric = config.model_testing.selected_test_metric
        self.best_model_name = None

    def pick_best_model(self):
        with open(self.test_metrics_file, 'r') as file:
            test_metrics = json.load(file)

        self.best_model_name = max(test_metrics, key=lambda model: test_metrics[model].get(self.selected_metric, float('-inf')))

    def save_best_model(self):
        best_model = joblib.load(os.path.join(self.config.model_training.models_dir, self.best_model_name + ".pkl"))
        joblib.dump(best_model, os.path.join(self.config.model_testing.root_dir, "model.pkl"))
