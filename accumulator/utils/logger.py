import logging
import sys


class Logger:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(Logger, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        from accumulator import config

        handler = logging.StreamHandler(sys.stdout)
        self.log = logging.getLogger(__name__)
        self.log.setLevel(config.LOG_LEVEL)
        self.log.addHandler(handler)
        formatter = logging.Formatter('%(asctime)s|%(levelname)s|%(name)s|%(message)s', datefmt='%Y-%m-%d %H:%M:%S,%f')
        handler.setFormatter(formatter)
