import io
import pandas as pd
import requests

from accumulator.config import DATAPORTAL_REQUEST_URL, STATION_PARAMETERS
from accumulator.parm import Parm


def fetch_parm() -> pd.DataFrame or int:
    """
    Fetch the latest tair data from DataPortal at the top of the hour for each station

    :return: pandas DataFrame of the latest tair data
    """
    parms = Parm(STATION_PARAMETERS)

    # TODO: allow for start and end times to be passed in
    parm_string = 'parm='.join([f"{parm[0]}:{parm[1]}&" for parm in parms.parameters])
    latest_parms = DATAPORTAL_REQUEST_URL.replace('<INSERT_PARMS_HERE>', parm_string)
    response = requests.get(latest_parms)

    if response.status_code == 200:
        print("\nfetch_parm complete with status code:", response.status_code)
        content = response.content.decode('utf-8')
        df = pd.read_csv(io.StringIO(content))
        return df

    else:
        print("Request failed with status code:", response.status_code)
        print("\nResponse:", response.text)
        return response.status_code
