from box import ConfigBox

from mlengine.data_read.read import read_csv_file


class StudentDataTransformer:
    def __init__(self, config: ConfigBox):
        self.config: ConfigBox = config
        self.df = None

    def transform(self):
        self.df = read_csv_file(filepath=self.config.data_file)
        self.df['total_score'] = self.df['math_score'] + self.df['reading_score'] + self.df['writing_score']
        self.df['average'] = self.df['total_score'] / 3

    def save(self):
        self.df.to_csv(self.config.data_file_transformed)
