import os
import json

ACC_DATASET_PATH = os.environ.get('ACC_DATASET_PATH')
CHILL_HOURS_VAR = os.environ.get('CHILL_HOURS_VAR')
DATAPORTAL_REQUEST_URL = os.environ.get('DATAPORTAL_REQUEST_URL')

models_to_run_string = os.environ.get('MODELS_TO_RUN')
MODELS_TO_RUN = json.loads(models_to_run_string)

station_parms_string = os.environ.get('STATION_PARAMETERS')
STATION_PARAMETERS = json.loads(station_parms_string)
