import logging
import sys

from accumulator.environment import LOG_LEVEL


def init_logging():
    """
        *IMPORTANT*
        This basicConfig only works if the container is run locally.
        If the container is run on AWS, the logging config will be set automatically by the AWS Lambda Python runtime
        which will render the basicConfig useless.
    """
    handler = logging.StreamHandler(sys.stdout)
    logging.basicConfig(
        level=LOG_LEVEL,
        format='%(asctime)s|%(levelname)s|%(name)s|%(message)s',
        datefmt='%Y-%m-%d %H:%M:%S,%f',
        handlers=[handler]
    )
    # This will set the root logger level to LOG_LEVEL regardless of whether the 
    # container is running in AWS or locally
    logging.getLogger().setLevel(LOG_LEVEL)  # Set root logger level


def print_logging_config(name: str):
    """
    Debug tool to figure out where the logging level changes
    :param name: Name of the location in the code where the logging level is being checked
    :return: None
    """
    root_logger = logging.getLogger()
    root_level = logging.getLevelName(root_logger.getEffectiveLevel())
    print(f"The root log level before {name} is {root_level}")
    for handler in root_logger.handlers:
        handler_level = logging.getLevelName(handler.level)
        print(f"A root handler has level {handler_level}")
