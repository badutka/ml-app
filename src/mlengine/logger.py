import logging
import coloredlogs
import os
from datetime import datetime

LOG_FILE = f'{datetime.now().strftime("%m_%d_%Y_%H_%M_%S")}.log'
LOG_PATH = os.path.join(os.getcwd(), 'logs')
os.makedirs(LOG_PATH, exist_ok=True)
LOG_FILE_PATH = os.path.join(LOG_PATH, LOG_FILE)
LOG_FORMAT = '[ %(asctime)s ] %(lineno)d %(name)s - %(levelname)s - %(message)s'


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

        logger.info("Logging initialized.")

    return logging.getLogger(LOG_FILE)


# Initialize logging when the module is imported
logger = initialize_logging()
