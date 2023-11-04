import abc

from mlengine.config.settings import settings
from mlengine.common.logger import logger
from mlengine.data_read.read import DataIngestion


class Pipeline(metaclass=abc.ABCMeta):
    """
    Interface for pipeline
    """

    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'run') and
                callable(subclass.run) or
                NotImplemented)

    @staticmethod
    @abc.abstractmethod
    def run() -> None:
        """Run the particular pipeline"""
        raise NotImplementedError


class PipelineRunner:
    """
    Responsible for encapsulating running any pipeline that fits the Pipeline Interface flow
    """

    def __init__(self, pipeline_object: Pipeline, stage_name: str):
        self.pipeline_object = pipeline_object
        self.stage_name = stage_name
        self.__stage_marker = 5 * '='
        self.__separator = 30 * '*'

    def run_pipeline(self):
        try:
            logger.info(f"{self.__stage_marker} {self.stage_name} started {self.__stage_marker}")
            self.pipeline_object.run()
            logger.info(f"{self.__stage_marker} {self.stage_name} completed {self.__stage_marker}\n{self.__separator}")
        except Exception as e:
            logger.exception(e)
            raise e


class DataIngestionPipeline(Pipeline):
    """
    Pipeline that run data ingestion process
    """

    @staticmethod
    def run():
        data_ingestion = DataIngestion(config=settings.data_ingestion)
        data_ingestion.download_file()
        data_ingestion.extract_zip_file()


def run_pipeline(option: str) -> None:
    """
    Facade for running pipeline chosen by option parameter

    :param option: str matched against a set of options to determine which pipeline to run
    """
    match option:
        case 'data_ingestion':
            pipeline = DataIngestionPipeline()
        case other:
            raise ValueError(f'Incorrect option: {other}.')

    runner = PipelineRunner(pipeline_object=pipeline, stage_name="Data Ingestion Stage")
    runner.run_pipeline()
