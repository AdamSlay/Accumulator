from datetime import datetime, timedelta
import json
import logging
import os

import pytz

log = logging.getLogger(__name__)

# Set the time stamp for the most recent hour(unless the current time is within 10 minutes of the top of the hour)
now_utc = datetime.now(pytz.timezone('UTC'))
if now_utc.minute <= 10:
    now_utc = now_utc - timedelta(hours=1)
DATE_TIME = now_utc.strftime('%Y-%m-%d %H:00:00')

# Path to the NetCDF4 dataset file
ACC_DATASET_PATH = os.environ.get('ACC_DATASET_PATH', 'default_path')

# Variable name for chill hours in the NetCDF4 file
CHILL_HOURS_VAR = os.environ.get('CHILL_HOURS_VAR', 'default_var')

# URL for the DataPortal request
DATAPORTAL_REQUEST_URL = os.environ.get('DATAPORTAL_REQUEST_URL', 'default_url')

# DataServer IP
DATASERVER_IP = os.environ.get('DATASERVER_IP', 'default_ip')

# DataServer Port
DATASERVER_PORT = int(os.environ.get('DATASERVER_PORT', 0))

# DataServer Dataset
DATASERVER_DATASET = os.environ.get('DATASERVER_DATASET', 'default_dataset')

# DataServer Request Type
DATASERVER_REQ_TYPE = os.environ.get('DATASERVER_REQ_TYPE', 'default_request_type')

# List of models to run
models_to_run_string = os.environ.get('MODELS_TO_RUN', '[]')
try:
    MODELS_TO_RUN = json.loads(models_to_run_string)
except json.JSONDecodeError:
    log.error(f"Invalid JSON for MODELS_TO_RUN: {models_to_run_string}")
    MODELS_TO_RUN = []

# List of station parameters
station_parms_string = os.environ.get('STATION_PARAMETERS', '[]')
try:
    STATION_PARAMETERS = json.loads(station_parms_string)
except json.JSONDecodeError:
    log.error(f"Invalid JSON for STATION_PARAMETERS: {station_parms_string}")
    STATION_PARAMETERS = []
