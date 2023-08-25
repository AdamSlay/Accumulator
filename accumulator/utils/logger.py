import logging
from logging.handlers import TimedRotatingFileHandler


def init_logging():
    # the handler below will rotate the log file every 30 days and keep 5 backups of the log file
    handler = TimedRotatingFileHandler('accumulator.log', when='D', interval=30, backupCount=5)
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s|%(levelname)s|%(name)s|%(message)s',
        datefmt='%Y-%m-%d %H:%M:%S,%f',
        handlers=[handler]
    )
