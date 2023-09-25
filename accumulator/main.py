import argparse
import socket
import json

from accumulator import config, logger
from accumulator.model_run import run_models
from accumulator.ncdf_update import write_ncdf
from accumulator.portal import fetch_station_data


def main(event=None, context=None):
    logger.log.info("Starting accumulator")

    try:
        ip_address = socket.gethostbyname(config.DATASERVER_HOST)
        logger.log.debug(f'Resolved IP address for \'{config.DATASERVER_HOST}\': {ip_address}')
    except socket.gaierror as e:
        logger.log.critical(f'Failed to resolve IP address for \'{config.DATASERVER_HOST}\': {e}')
        return {
            'statusCode': 500,
            'body': f'Failed to resolve IP address for \'{config.DATASERVER_HOST}\': {e}'
        }

    try:
        station_obs_data = fetch_station_data()
        updated_accum_data = run_models(station_obs_data)
        write_ncdf(updated_accum_data)

    except (socket.error, json.JSONDecodeError) as e:
        logger.log.critical(f"An error occurred while fetching station data or processing the response: {e}")
        return {
            'statusCode': 500,
            'body': f'A socket error occurred: {e}'
        }
    except (PermissionError, OSError, FileNotFoundError) as e:
        logger.log.critical(f"An error occurred while accessing or modifying the NetCDF4 dataset at {config.ACCUM_DATASET_PATH}: {e}")
        return {
            'statusCode': 500,
            'body': f'A file error occurred: {e}'
        }
    except Exception as e:
        logger.log.critical(f"An unexpected error occurred: {e}")
        return {
            'statusCode': 500,
            'body': f'An unexpected error occurred: {e}'
        }

    finally:
        logger.log.info("Finished running accumulator")

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
