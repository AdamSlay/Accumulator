import logging
import sys
import socket
import json

from accumulator.utils.logger import init_logging
from accumulator.model_run import run_models
from accumulator.ncdf_update import write_ncdf
from accumulator.portal import fetch_station_data
from accumulator.environment import ACCUM_DATASET_PATH, LOG_PATH


def main():
    init_logging()
    log = logging.getLogger(__name__)

    log.info("Starting accumulator")

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


if __name__ == '__main__':
    exit(main())
