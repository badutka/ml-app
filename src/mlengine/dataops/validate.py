import pydantic
from box import ConfigBox
import os
from pathlib import Path

from mlengine.common.logger import logger
from mlengine.common.utils import create_directories
from mlengine.common.exceptions import MissingCriticalFileException
from mlengine.data_read.read import read_csv_file


class StudentDataTypesValidator(pydantic.BaseModel):
    gender: pydantic.StrictStr
    race_ethnicity: pydantic.StrictStr
    parental_level_of_education: pydantic.StrictStr
    lunch: pydantic.StrictStr
    test_preparation_course: pydantic.StrictStr
    math_score: pydantic.StrictInt
    reading_score: pydantic.StrictInt
    writing_score: pydantic.StrictInt


class StudentTransformedDataTypesValidator(pydantic.BaseModel):
    gender: pydantic.StrictStr
    race_ethnicity: pydantic.StrictStr
    parental_level_of_education: pydantic.StrictStr
    lunch: pydantic.StrictStr
    test_preparation_course: pydantic.StrictStr
    math_score: pydantic.StrictInt
    reading_score: pydantic.StrictInt
    writing_score: pydantic.StrictInt
    total_score: pydantic.StrictInt
    average: pydantic.StrictFloat


class StudentDataValidator:
    def __init__(self, config: ConfigBox):
        self.config: ConfigBox = config
        self.data_file_path: Path = self.config.data_ingestion.root_dir
        self.data_file_name: str = self.config.data_ingestion.data_file
        self.data_file: Path = Path(os.path.join(self.data_file_path, self.data_file_name))

    def validate_data(self):
        try:
            df = read_csv_file(self.data_file)
            data_list = [StudentDataTypesValidator(**row) for _, row in df.iterrows()]
            logger.info(f'Successful validation of data file {self.data_file} via Pydantic strict types')
        except Exception as e:
            raise e


class StudentTransformedDataValidator:
    def __init__(self, config: ConfigBox):
        self.config: ConfigBox = config.data_transformation
        self.data_file_path: Path = self.config.root_dir
        self.data_file_name: str = self.config.data_file_tnsf
        self.data_file: Path = Path(os.path.join(self.data_file_path, self.data_file_name))

    def validate_data(self):
        try:
            df = read_csv_file(self.data_file)
            data_list = [StudentDataTypesValidator(**row) for _, row in df.iterrows()]
            logger.info(f'Successful validation of data file {self.data_file} via Pydantic strict types')
        except Exception as e:
            raise e


class FileValidator:
    def __init__(self, config: ConfigBox, config_req_files: ConfigBox):
        self.config: ConfigBox = config
        self.config_req_files: ConfigBox = config_req_files
        self._create_dirs()

    def _create_dirs(self):
        create_directories([self.config.root_dir])

    def validate_all_files_exist(self):
        try:
            files_in_data_root_dir = os.listdir(self.config_req_files.root_dir)
            statuses = []
            messages = []

            for file in self.config.req_files:
                validation_status = file in files_in_data_root_dir
                statuses.append(validation_status)

                msg = f"Validation status: {validation_status} for file: {file}"
                messages.append(msg)

                logger.info(msg)

            status = all(statuses)

            with open(os.path.join(self.config.root_dir, self.config.status_file), 'w') as f:
                for msg in messages:
                    f.write(msg + "\n")
                f.write(f"Overall status: {status}")

            if not status:
                raise MissingCriticalFileException('VLD_EX_001', 'Validation failed for critical file(s). Check the logged status file for more information.')

        except Exception as e:
            raise e
