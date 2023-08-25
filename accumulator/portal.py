import io
import logging
import time

import pandas as pd
import requests

from accumulator.config import DATAPORTAL_REQUEST_URL, STATION_PARAMETERS
from accumulator.parm import Parm

log = logging.getLogger(__name__)


def fetch_parm() -> pd.DataFrame:
    """
    Fetch the latest tair data from DataPortal at the top of the hour for each station

    :return: pandas DataFrame of the latest tair data
    """
    parms = Parm(STATION_PARAMETERS)

    # TODO: allow for start and end times to be passed in
    parm_string = 'parm='.join([f"{parm[0]}:{parm[1]}&" for parm in parms.parameters])
    latest_parms = DATAPORTAL_REQUEST_URL.replace('<INSERT_PARMS_HERE>', parm_string)

    max_retries = 3
    retry_delay = 5  # seconds

    for i in range(max_retries):
        try:
            response = requests.get(latest_parms)
            response.raise_for_status()  # This will raise an HTTPError if the status code is not 200
            content = response.content.decode('utf-8')
            df = pd.read_csv(io.StringIO(content))
            return df  # return the DataFrame if the request was successful, and break out of the loop
        except (requests.exceptions.RequestException, UnicodeDecodeError, pd.errors.ParserError) as e:
            log.error(f"Error occurred: {e}. Retry {i + 1} of {max_retries}")
            time.sleep(retry_delay)

    raise Exception("Request failed after maximum retries")
