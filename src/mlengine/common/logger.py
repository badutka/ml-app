import logging
import coloredlogs
import os
from datetime import datetime

LOG_FILE = f'{datetime.now().strftime("%m_%d_%Y_%H_%M_%S")}.log'
LOG_PATH = os.path.join(os.getcwd(), 'logs')
os.makedirs(LOG_PATH, exist_ok=True)
LOG_FILE_PATH = os.path.join(LOG_PATH, LOG_FILE)
LOG_FORMAT = '[ %(asctime)s ] %(lineno)d %(name)s - %(levelname)s - %(message)s'


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Logger(metaclass=Singleton):
    def __init__(self):
        pass

    @staticmethod
    def initialize_logging():
        if not logging.root.handlers:
            formatter = logging.Formatter(LOG_FORMAT)
            logger = logging.getLogger(LOG_FILE)

            logger.setLevel(logging.DEBUG)

            ch = logging.StreamHandler()
            ch.setLevel(logging.DEBUG)
            ch.setFormatter(formatter)
            logger.addHandler(ch)

            fh = logging.FileHandler(LOG_FILE_PATH)
            fh.setLevel(logging.DEBUG)
            formatter = logging.Formatter(LOG_FORMAT)
            fh.setFormatter(formatter)
            logger.addHandler(fh)

            coloredlogs.install(
                logger=logger,
                level_styles={
                    'debug': {'color': 'blue'},
                    'info': {'color': 'green'},
                    'warning': {'color': 'yellow'},
                    'error': {'color': 'red'},
                    'critical': {'color': 'red', 'bold': True}
                })

            logger.info(f"Logging initialized.\n{30*'*'}")

        return logging.getLogger(LOG_FILE)


logger = Logger().initialize_logging()

# class LoggerSingleton:
#     _instance = None
#
#     def __new__(cls):
#         if cls._instance is None:
#             cls._instance = super(LoggerSingleton, cls).__new__(cls)
#             cls._instance.initialize_logging()
#         return cls._instance
#
#     def initialize_logging(self):
#         if not logging.root.handlers:
#             formatter = logging.Formatter(LOG_FORMAT)
#             self.logger = logging.getLogger("my_logger")
#
#             self.logger.setLevel(logging.DEBUG)
#
#             ch = logging.StreamHandler()
#             ch.setLevel(logging.DEBUG)
#             ch.setFormatter(formatter)
#             self.logger.addHandler(ch)
#
#             fh = logging.FileHandler(LOG_FILE)
#             fh.setLevel(logging.DEBUG)
#             formatter = logging.Formatter(LOG_FORMAT)
#             fh.setFormatter(formatter)
#             self.logger.addHandler(fh)
#
#             coloredlogs.install(
#                 logger=self.logger,
#                 level_styles={
#                     'debug': {'color': 'blue'},
#                     'info': {'color': 'green'},
#                     'warning': {'color': 'yellow'},
#                     'error': {'color': 'red'},
#                     'critical': {'color': 'red', 'bold': True}
#                 })
#
#             self.logger.info("Logging initialized")
#
#     def get_logger(self):
#         return self.logger
#
#
# logger_instance = LoggerSingleton()
#
# logger = logger_instance.get_logger()
