import logging
from logging.handlers import TimedRotatingFileHandler

from accumulator.ncdf_update import write_ncdf
from accumulator.portal import fetch_parm
from accumulator.utils import set_time_stamp, run_models


def main():
    handler = TimedRotatingFileHandler('accumulator.log', when='D', interval=30, backupCount=5)
    logging.basicConfig(level=logging.INFO, handlers=[handler])

    try:
        stations_csv = fetch_parm()
        updated_accumulation = run_models(stations_csv)
        new_time_stamp = set_time_stamp()
        write_ncdf(updated_accumulation, new_time_stamp)
    except Exception as e:
        logging.error(f"An error occurred: {e}")

if __name__ == '__main__':
    main()
