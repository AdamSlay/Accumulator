import io
import pandas as pd
import requests

from parm import Parm


def fetch_parm(parms: Parm) -> pd.DataFrame or int:
    """
    Fetch the latest tair data from DataPortal at the top of the hour for each station
    :param parms: Parm object which contains the parameters to fetch
    :return: pandas DataFrame of the latest tair data
    """

    # Make a GET request to a URL
    parm_string = 'parm='.join([f"{parm[0]}:{parm[1]}&" for parm in parms.parameters])
    tair_latest = f"http://portal.dev.okmeso.net/data/api/rest/times/latest?parm={parm_string}fmt=csv"
    response = requests.get(tair_latest)

    # Check the response status code
    if response.status_code == 200:
        print("\nfetch_parm complete with status code:", response.status_code)

        # Read the content of the response as CSV
        content = response.content.decode('utf-8')
        df = pd.read_csv(io.StringIO(content))

        return df
    else:
        print("Request failed with status code:", response.status_code)
        print("\nResponse:", response.text)
        return response.status_code
