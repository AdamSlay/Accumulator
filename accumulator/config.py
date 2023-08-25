import json
import logging
import os

log = logging.getLogger(__name__)


# Path to the NetCDF4 dataset file
ACC_DATASET_PATH = os.environ.get('ACC_DATASET_PATH', 'default_path')

# Variable name for chill hours in the NetCDF4 file
CHILL_HOURS_VAR = os.environ.get('CHILL_HOURS_VAR', 'default_var')

# URL for the DataPortal request
DATAPORTAL_REQUEST_URL = os.environ.get('DATAPORTAL_REQUEST_URL', 'default_url')

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
