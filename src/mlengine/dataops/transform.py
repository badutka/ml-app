from box import ConfigBox
import os
from pathlib import Path

from mlengine.data_read.read import read_csv_file


class StudentDataTransformer:
    def __init__(self, config: ConfigBox):
        self.config: ConfigBox = config
        self.data_file: Path = Path(os.path.join(self.config.data_ingestion.root_dir, self.config.data_ingestion.data_file))
        self.data_file_tnsf: Path = Path(os.path.join(self.config.data_transformation.root_dir, self.config.data_transformation.data_file_tnsf))
        self.df = None

    def transform(self):
        self.df = read_csv_file(filepath=self.data_file)
        # self.df['total_score'] = self.df['math_score'] + self.df['reading_score'] + self.df['writing_score']
        # self.df['average'] = self.df['total_score'] / 3

    def save(self):
        self.df.to_csv(self.data_file_tnsf)
