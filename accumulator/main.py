import argparse
import logging
import socket
import json

from accumulator.utils.logger import init_logging
from accumulator.model_run import run_models
from accumulator.ncdf_update import write_ncdf
from accumulator.portal import fetch_station_data
from accumulator.environment import ACCUM_DATASET_PATH, LOG_PATH


def main(event=None, context=None):
    init_logging()
    log = logging.getLogger(__name__)

    log.info("Starting accumulator")

    try:
        ip_address = socket.gethostbyname('portal.dev.okmeso.net')
        log.debug(f'IP address of portal.dev.okmeso.net is {ip_address}')
    except socket.gaierror as e:
        log.error(f'Failed to get IP address of portal.dev.okmeso.net: {e}')
        return {
            'statusCode': 500,
            'body': 'Failed to get IP address of portal.dev.okmeso.net'
        }

    try:
        station_obs_data = fetch_station_data()
        updated_accum_data = run_models(station_obs_data)
        write_ncdf(updated_accum_data)

    except (socket.error, json.JSONDecodeError) as e:
        log.error(f"An error occurred while fetching station data or processing the response: {e}")
        return {
            'statusCode': 500,
            'body': 'A socket error occurred'
        }
    except (PermissionError, OSError, FileNotFoundError) as e:
        log.error(f"An error occurred while accessing or modifying the NetCDF4 dataset at {ACCUM_DATASET_PATH}: {e}")
        return {
            'statusCode': 500,
            'body': 'A file error occurred'
        }
    except Exception as e:
        log.error(f"An unexpected error occurred. Please check the logs at {LOG_PATH} for more details: {e}")
        return {
            'statusCode': 500,
            'body': 'An unexpected error occurred'
        }

    finally:
        log.info("Finished running accumulator")

    return {
        'statusCode': 200,
        'body': 'Function completed'
    }


def lambda_handler(event, context):
    # Call your main function and return its result
    return main(event, context)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--local", action="store_true",
                        help="run the application locally without aws lambda invocation")
    # add argument for lambda event
    parser.add_argument("--event", action="store_true", help="lambda event")
    parser.add_argument("--context", action="store_true", help="lambda context")

    args = parser.parse_args()
    lambda_handler(args.event, args.context)
