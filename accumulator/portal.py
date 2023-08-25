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
    try:
        # Create a socket object and connect to the server
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((DATASERVER_IP, DATASERVER_PORT))
        query = build_query()
        request_bytes = json.dumps(query).encode('utf-8')
        sock.sendall(request_bytes)

        # Receive the response
        response = receive_response(sock)
        log_connection_status(response)
        sock.close()

        # Convert the response to a DataFrame
        data = convert_resp_to_df(response)
        return data

    except socket.error as e:
        log.error(f"A socket error occurred while fetching station data: {e}")
        raise e
    except json.JSONDecodeError as e:
        log.error(f"A JSON decode error occurred while parsing the response: {e}")
        raise e
    except Exception as e:
        log.error(f"An error occurred while fetching station data: {e}")
        raise e

def build_query():
    """
    Build the query to send to the DataServer based on the environment variables

    :return: The query as a JSON object
    """
    return {
        "type": DATASERVER_REQ_TYPE,
        "dataset": DATASERVER_DATASET,
        "date": DATE_TIME,
        "variables": STATION_PARAMETERS,
    }


def receive_response(sock):
    """
    Receive the response from the DataServer in chunks of 1024 bytes and return the response as a JSON object

    :param sock: The socket object to receive the response from
    :return: The response as a JSON object
    """
    response_bytes = b''
    while True:
        part = sock.recv(1024)
        if not part:
            break  # The response has been fully received
        response_bytes += part
    return json.loads(response_bytes.decode('utf-8'))


def log_connection_status(response):
    """
    Log the connection status based on the response from the DataServer
    :param response: The response from the DataServer
    :return: None
    """
    if response['success']:
        log.info(f"Successfully connected to DataServer at {DATASERVER_IP}:{DATASERVER_PORT}")
    else:
        log.error(f"Failed to connect to DataServer at {DATASERVER_IP}:{DATASERVER_PORT}")
        raise ConnectionError(f"Failed to connect to DataServer at {DATASERVER_IP}:{DATASERVER_PORT}")


def convert_resp_to_df(response):
    """
    Convert the response from the DataServer to a pandas DataFrame

    :param response: The response from the DataServer
    :return: pandas DataFrame of the response
    """
    data = pd.DataFrame()
    for parameter, values in response['response'].items():
        data[parameter] = values['data']
    return data.set_index('stid')
