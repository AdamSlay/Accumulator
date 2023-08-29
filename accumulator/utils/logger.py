import logging
from logging.handlers import TimedRotatingFileHandler
from accumulator.environment import LOG_LEVEL, LOG_PATH


def init_logging():
    # the handler below will rotate the log file every 30 days and keep 5 backups of the log file
    handler = TimedRotatingFileHandler(LOG_PATH, when='D', interval=30, backupCount=5)
    logging.basicConfig(
        level=LOG_LEVEL,
        format='%(asctime)s|%(levelname)s|%(name)s|%(message)s',
        datefmt='%Y-%m-%d %H:%M:%S,%f',
        handlers=[handler]
    )
