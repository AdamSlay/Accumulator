import json
import socket

import pandas as pd

from accumulator import config, logger


def fetch_station_data() -> pd.DataFrame:
    """
    Fetch the latest tair data from DataServer at the top of the hour for each station

    :return: pandas DataFrame of the latest tair data
    """
    logger.log.info(f"Connecting to DataServer at {config.DATASERVER_HOST}:{config.DATASERVER_PORT}")

    for attempt in range(config.SOCKET_ATTEMPTS):  # Retry 3 times
        try:
            # Create a socket object and connect to DataServer
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(config.DATASERVER_TIMEOUT)
                sock.connect((config.DATASERVER_HOST, config.DATASERVER_PORT))
                logger.log.debug("Connected to DataServer")

                query = build_query()
                request_bytes = json.dumps(query).encode('utf-8')
                logger.log.debug("Sending request")
                sock.sendall(request_bytes)

                # Receive the response
                logger.log.debug("Receiving response")
                response = receive_response(sock)
                logger.log.debug("Response received")
                log_connection_status(response)

            # Convert the response to a DataFrame
            data = convert_resp_to_df(response)
            return data  # If the connection was successful, return the data and exit the loop

        except socket.error as e:
            if attempt < (config.SOCKET_ATTEMPTS - 1):
                # If this was not the last attempt, log the error and continue
                logger.log.warning(f"Connection Attempt {attempt} of {config.SOCKET_ATTEMPTS}: A socket error occurred while fetching station data: {e}")
                continue
            else:
                # If this was the last attempt, log the error and raise the exception
                logger.log.error(f"A socket error occurred while fetching station data: {e}")
                raise
        except json.JSONDecodeError as e:
            logger.log.error(f"A JSON decode error occurred while parsing the response: {e}")
            raise
        except Exception as e:
            logger.log.error(f"An error occurred while fetching station data: {e}")
            raise


def build_query(ds_req_type=config.DATASERVER_REQ_TYPE,
                ds_dataset=config.DATASERVER_DATASET,
                ds_date=config.DATE_TIME,
                ds_variables=config.STATION_PARAMETERS) -> dict[str, any]:
    """
    Build the query to send to the DataServer based on the environment variables

    :return: The query as a JSON object
    """
    return {
        "type": ds_req_type,
        "dataset": ds_dataset,
        "date": ds_date,
        "variables": ds_variables,
    }


def receive_response(sock: socket.socket) -> dict[str, any]:
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


def log_connection_status(response: dict[str, any]) -> None:
    """
    Log the connection status based on the response from the DataServer
    :param response: The response from the DataServer
    :return: None
    """
    if response['success']:
        logger.log.info(f"Successfully connected to DataServer at {config.DATASERVER_HOST}:{config.DATASERVER_PORT}")
    else:
        logger.log.error(f"Failed to connect to DataServer at {config.DATASERVER_HOST}:{config.DATASERVER_PORT}")
        raise ConnectionError(f"Failed to connect to DataServer at {config.DATASERVER_HOST}:{config.DATASERVER_PORT}")


def convert_resp_to_df(response: dict[str, any]) -> pd.DataFrame:
    """
    Convert the response from the DataServer to a pandas DataFrame

    :param response: The response from the DataServer
    :return: pandas DataFrame of the response
    """
    data = pd.DataFrame()
    for parameter, values in response['response'].items():
        data[parameter] = values['data']
    data = data.set_index('stid')
    return data
