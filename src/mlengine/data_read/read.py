from box import ConfigBox
from pathlib import Path
import os
import pandas as pd
import urllib.request as request
import zipfile
from mlengine.common.logger import logger
from mlengine.common.utils import create_directories


class DataIngestion:
    def __init__(self, config: ConfigBox):
        self.config = config.data_ingestion
        self._create_dirs()

    def _create_dirs(self):
        create_directories([self.config.root_dir])

    def download_file(self):
        if not os.path.exists(self.config.zipped_file):
            filename, headers = request.urlretrieve(
                url=self.config.source_URL,
                filename=self.config.zipped_file
            )
            logger.info(f"{filename} downloaded. Headers: \n{headers}")
        else:
            logger.info(f"File already exists")

    def extract_zip_file(self):
        """
        zip_file_path: str
        Extracts the zip file into the data directory
        Function returns None
        """
        unzip_path = self.config.unzip_dir
        os.makedirs(unzip_path, exist_ok=True)
        with zipfile.ZipFile(self.config.zipped_file, 'r') as zip_ref:
            zip_ref.extractall(unzip_path)


def read_csv_file(filepath: Path) -> pd.DataFrame:
    return pd.read_csv(filepath_or_buffer=filepath, delimiter=',')
