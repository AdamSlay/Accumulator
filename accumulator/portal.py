import io
import json
import logging
import socket
import time

import pandas as pd
import requests

from accumulator.environment import DATAPORTAL_REQUEST_URL, STATION_PARAMETERS
from accumulator.parm import Parm

log = logging.getLogger(__name__)


def fetch_station_data() -> pd.DataFrame:
    """
    Fetch the latest tair data from DataPortal at the top of the hour for each station

    :return: pandas DataFrame of the latest tair data
    """
    parms = Parm(STATION_PARAMETERS)

    # TODO: allow for start and end times to be passed in
    # TODO: use DataServer
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


def data_server_fetch():
    """
    Fetch the latest tair data from DataServer at the top of the hour for each station

    the public facing IP address is: 54.184.161.68 on tcp port 10000 which is running on portal-04.aws

    :return: pandas DataFrame of the latest tair data
    """
    query = {
        "type": "map-netcdf",
        "dataset": "edu.ou.mesonet.standard",
        "date": "2023-08-22 06:00:00",
        "variables": [{"id": "tair", "units": "fahr"}],
    }

    # Define the server and port
    server = "54.184.161.68"
    port = 10000

    # Create a socket object and connect to the server
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((server, port))
    request_bytes = json.dumps(query).encode('utf-8')
    s.sendall(request_bytes)

    # Receive the response
    response_bytes = s.recv(1024)
    response = json.loads(response_bytes.decode('utf-8'))

    # Don't forget to close the socket when you're done
    s.close()

    log.info(f"Response from DataServer: {response}")

    # Convert the response to a pandas DataFrame and return it
    return pd.DataFrame(response)
