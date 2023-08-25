import logging

from accumulator.logger import init_logging
from accumulator.ncdf_update import write_ncdf
from accumulator.portal import fetch_parm
from accumulator.utils import set_time_stamp, run_models


def main():
    init_logging()
    log = logging.getLogger(__name__)

    log.info("Starting accumulator")
    try:
        stations_csv = fetch_parm()
        updated_accumulation = run_models(stations_csv)
        new_time_stamp = set_time_stamp()
        write_ncdf(updated_accumulation, new_time_stamp)
    except Exception as e:
        log.error(f"An error occurred: {e}")

    log.info("Finished running accumulator")


if __name__ == '__main__':
    main()
