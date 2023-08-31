import logging
import sys

from accumulator.environment import LOG_LEVEL

def init_logging():
    handler = logging.StreamHandler(sys.stdout)
    logging.basicConfig(
        level=LOG_LEVEL,
        format='%(asctime)s|%(levelname)s|%(name)s|%(message)s',
        datefmt='%Y-%m-%d %H:%M:%S,%f',
        handlers=[handler]
    )
