import logging
import sys

from accumulator.utils.logger import init_logging
from accumulator.model_run import run_models
from accumulator.ncdf_update import write_ncdf
from accumulator.portal import fetch_station_data


def main():
    init_logging()
    log = logging.getLogger(__name__)

    log.info("Starting accumulator")
    try:
        station_obs_data = fetch_station_data()
        updated_accum_data = run_models(station_obs_data)
        write_ncdf(updated_accum_data)
    except Exception as e:
        log.error(f"An error occurred: {e}")
        sys.exit(1)

    log.info("Finished running accumulator")


if __name__ == '__main__':
    main()
