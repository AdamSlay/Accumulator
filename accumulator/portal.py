import json
import logging
import socket

import pandas as pd

from accumulator.environment import STATION_PARAMETERS, DATASERVER_DATASET, DATASERVER_IP, \
    DATASERVER_PORT, DATASERVER_REQ_TYPE, DATE_TIME

log = logging.getLogger(__name__)


def fetch_station_data():
    """
    Fetch the latest tair data from DataServer at the top of the hour for each station

    :return: pandas DataFrame of the latest tair data
    """
    print(DATE_TIME)
    query = {
        "type": DATASERVER_REQ_TYPE,
        "dataset": DATASERVER_DATASET,
        "date": DATE_TIME,
        "variables": STATION_PARAMETERS,
    }

    # Create a socket object and connect to the server
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((DATASERVER_IP, DATASERVER_PORT))
    request_bytes = json.dumps(query).encode('utf-8')
    sock.sendall(request_bytes)

    # Receive the response in chunks and concatenate them
    response_bytes = b''
    while True:
        part = sock.recv(1024)
        if not part:
            break  # The response has been fully received
        response_bytes += part
    
    response = json.loads(response_bytes.decode('utf-8'))
    sock.close()

    if response['success']:
        log.info(f"Successfully connected to DataServer at {DATASERVER_IP}:{DATASERVER_PORT}")
    else:
        log.error(f"Failed to connect to DataServer at {DATASERVER_IP}:{DATASERVER_PORT}")

    data = pd.DataFrame()
    for parameter, values in response['response'].items():
        data[parameter] = values['data']
    data = data.set_index('stid')
    print(data)
    return data
