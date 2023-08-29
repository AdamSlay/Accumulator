import logging
import sys
import socket
import json

from accumulator.utils.logger import init_logging
from accumulator.model_run import run_models
from accumulator.ncdf_update import write_ncdf
from accumulator.portal import fetch_station_data
from accumulator.environment import ACCUM_DATASET_PATH


def main():
    init_logging()
    log = logging.getLogger(__name__)

    log.info("Starting accumulator")

    try:
        station_obs_data = fetch_station_data()
        updated_accum_data = run_models(station_obs_data)
        write_ncdf(updated_accum_data)

    except (socket.error, json.JSONDecodeError) as e:
        log.error(f"A network or data error occurred: {e}")
        sys.exit(2)
    except FileNotFoundError as e:
        log.error(f"NetCDF4 file not found at {ACCUM_DATASET_PATH}: {e}")
        sys.exit(3)
    except (PermissionError, OSError) as e:
        log.error(f"Permission denied or OSError for {ACCUM_DATASET_PATH}: {e}")
        sys.exit(4)
    except Exception as e:
        log.error(f"An unexpected error occurred: {e}")
        sys.exit(1)

    log.info("Finished running accumulator")


if __name__ == '__main__':
    main()
