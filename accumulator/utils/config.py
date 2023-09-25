from datetime import datetime, timedelta
import logging
import os
import pytz
import toml


class Config:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Config, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        log = logging.getLogger(__name__)

        # Set the time stamp for the most recent hour(unless current time is within 5 minutes of the top of the hour)
        now_utc = datetime.now(pytz.timezone('UTC'))
        if now_utc.minute <= 5:
            now_utc = now_utc - timedelta(hours=1)
        self.DATE_TIME = now_utc.strftime('%Y-%m-%d %H:00:00')

        # ENVIRONMENT VARIABLES
        self.ACCUM_DATASET_PATH = os.environ.get('ACCUM_DATASET_PATH', 'default_path')
        self.DATASERVER_HOST = os.environ.get('DATASERVER_HOST', 'default_ip')
        self.DATASERVER_PORT = int(os.environ.get('DATASERVER_PORT', 0))

        # CONFIG 
        config = toml.load('etc/config/config.toml')
        self.CHILL_HOURS_VAR = config['settings'].get('CHILL_HOURS_VAR', 'chill_hours')
        self.DATASERVER_DATASET = config['settings'].get('DATASERVER_DATASET', 'edu.ou.mesonet.standard')
        self.DATASERVER_REQ_TYPE = config['settings'].get('DATASERVER_REQ_TYPE', 'map-netcdf')
        self.SOCKET_ATTEMPTS = config['settings'].get('SOCKET_ATTEMPTS', 3)
        self.DATASERVER_TIMEOUT = config['settings'].get('DATASERVER_TIMEOUT', 30)
        self.MODELS_TO_RUN = config['settings'].get('MODELS_TO_RUN', [])
        self.STATION_PARAMETERS = config['settings'].get('STATION_PARAMETERS', [])
        self.LOG_LEVEL = config['settings'].get('LOG_LEVEL', 'INFO')
        self.LOG_PATH = config['settings'].get('LOG_PATH', 'accumulator.log')
