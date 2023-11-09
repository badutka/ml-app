import abc

from mlengine.config.settings import settings
from mlengine.common.logger import logger
from mlengine.data_read.read import DataIngestion
from mlengine.common.utils import create_directories
from mlengine.dataops.validate import FileValidator, StudentDataValidator, StudentTransformedDataValidator
from mlengine.dataops.transform import StudentDataTransformer
from mlengine.dataops.split import DataSplitter
from mlengine.features.prep import Preprocessor
from mlengine.models.train import ModelTrainer
from mlengine.models.evaluate import ModelEvaluator


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
    Pipeline that runs data ingestion process
    """

    @staticmethod
    def run():
        create_directories([settings.artifacts_root])
        data_ingestion = DataIngestion(config=settings.data_ingestion)
        data_ingestion.download_file()
        data_ingestion.extract_zip_file()


class DataValidationPreTransformPipeline(Pipeline):
    """
    Pipeline that runs data validation process
    """

    @staticmethod
    def run():
        file_validator = FileValidator(config=settings.data_validation)
        file_validator.validate_all_files_exist()
        data_validator = StudentDataValidator(config=settings.data_validation)
        data_validator.validate_data()


class DataTransformationPipeline(Pipeline):
    """
    Pipeline that runs data transformation process
    """

    @staticmethod
    def run():
        file_validator = FileValidator(config=settings.data_transformation)
        file_validator.validate_all_files_exist()
        data_transformer = StudentDataTransformer(config=settings.data_transformation)
        data_transformer.transform()
        data_transformer.save()


class DataValidationPostTransformPipeline(Pipeline):
    """
    Pipeline that runs data transformation process
    """

    @staticmethod
    def run():
        file_validator = FileValidator(config=settings.data_validation_post_t)
        file_validator.validate_all_files_exist()
        data_validator = StudentTransformedDataValidator(config=settings.data_validation_post_t)
        data_validator.validate_data()


class DataSplitPipeline(Pipeline):
    """
    Pipeline that runs dataset split process
    """

    @staticmethod
    def run():
        file_validator = FileValidator(config=settings.data_split)
        file_validator.validate_all_files_exist()
        data_splitter = DataSplitter(config=settings)
        data_splitter.train_validate_test_split()


class ModelPreprocessingPipeline(Pipeline):
    """
    Pipeline that runs data preprocessing (feature engineering)
    """

    @staticmethod
    def run():
        file_validator = FileValidator(config=settings.model_preprocessing)
        file_validator.validate_all_files_exist()
        data_splitter = Preprocessor(config=settings.model_preprocessing)
        data_splitter.get_features_data()
        data_splitter.setup_preprocessing_pipeline()
        data_splitter.fit_train_data()
        data_splitter.save_preprocessing_pipeline()


class ModelTrainingPipeline(Pipeline):
    """
    Pipeline that runs model training process
    """

    @staticmethod
    def run():
        file_validator = FileValidator(config=settings.model_training)
        file_validator.validate_all_files_exist()
        data_splitter = ModelTrainer(config=settings.model_training)
        data_splitter.get_training_data()
        data_splitter.preprocess_training_data()
        data_splitter.train_models()
        model_evaluator = ModelEvaluator(config=settings.model_training)
        model_evaluator.load_models()
        model_evaluator.load_data_files()
        model_evaluator.preprocess_data()
        model_evaluator.save_regression_evaluation()


class ModelValidationPipeline(Pipeline):
    """
    Pipeline that runs model training process
    """

    @staticmethod
    def run():
        file_validator = FileValidator(config=settings.model_validation)
        file_validator.validate_all_files_exist()
        model_evaluator = ModelEvaluator(config=settings.model_validation)
        model_evaluator.load_models()
        model_evaluator.load_data_files()
        model_evaluator.preprocess_data()
        model_evaluator.save_regression_evaluation()


class ModelTestingPipeline(Pipeline):
    """
    Pipeline that runs model testing process
    """

    @staticmethod
    def run():
        file_validator = FileValidator(config=settings.model_testing)
        file_validator.validate_all_files_exist()
        model_evaluator = ModelEvaluator(config=settings.model_testing)
        model_evaluator.load_models()
        model_evaluator.load_data_files()
        model_evaluator.preprocess_data()
        model_evaluator.save_regression_evaluation()


def run_pipeline(option: str) -> None:
    """
    Facade for running pipeline chosen by option parameter

    :param option: str matched against a set of options to determine which pipeline to run
    """
    match option:
        case 'data_ingestion':
            stage_name = "Data Ingestion"
            pipeline = DataIngestionPipeline()
        case 'data_validation_pre_t':
            stage_name = "Data Validation (Pre-T)"
            pipeline = DataValidationPreTransformPipeline()
        case 'data_transformation':
            stage_name = "Data Transformation"
            pipeline = DataTransformationPipeline()
        case 'data_validation_post_t':
            stage_name = "Data Validation (Post-T)"
            pipeline = DataValidationPostTransformPipeline()
        case 'data_split':
            stage_name = "Dataset Split"
            pipeline = DataSplitPipeline()
        case 'model_preprocessing':
            stage_name = "Model Preprocessing"
            pipeline = ModelPreprocessingPipeline()
        case 'model_training':
            stage_name = "Model Training"
            pipeline = ModelTrainingPipeline()
        case 'model_validation':
            stage_name = "Model Validation"
            pipeline = ModelValidationPipeline()
        case 'model_testing':
            stage_name = "Model Testing"
            pipeline = ModelTestingPipeline()
        case other:
            raise ValueError(f'Incorrect option: {other}.')

    runner = PipelineRunner(pipeline_object=pipeline, stage_name=stage_name)
    runner.run_pipeline()
