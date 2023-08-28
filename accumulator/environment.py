from datetime import datetime, timedelta
import logging
import os
import pytz
import toml

log = logging.getLogger(__name__)

# Set the time stamp for the most recent hour(unless the current time is within 10 minutes of the top of the hour)
now_utc = datetime.now(pytz.timezone('UTC'))
if now_utc.minute <= 10:
    now_utc = now_utc - timedelta(hours=1)
DATE_TIME = now_utc.strftime('%Y-%m-%d %H:00:00')

# ENVIRONMENT VARIABLES
ACCUM_DATASET_PATH = os.environ.get('ACCUM_DATASET_PATH', 'default_path')
DATASERVER_IP = os.environ.get('DATASERVER_IP', 'default_ip')
DATASERVER_PORT = int(os.environ.get('DATASERVER_PORT', 0))

# CONFIG 
config = toml.load('etc/config/config.toml')
CHILL_HOURS_VAR = config['settings'].get('CHILL_HOURS_VAR', 'chill_hours')
DATASERVER_DATASET = config['settings'].get('DATASERVER_DATASET', 'edu.ou.mesonet.standard')
DATASERVER_REQ_TYPE = config['settings'].get('DATASERVER_REQ_TYPE', 'map-netcdf')
MODELS_TO_RUN = config['settings'].get('MODELS_TO_RUN', [])
STATION_PARAMETERS = config['settings'].get('STATION_PARAMETERS', [])
LOG_LEVEL = config['settings'].get('LOG_LEVEL', 'INFO')
LOG_FILE = config['settings'].get('LOG_FILE', 'accumulator.log')
