from datetime import datetime

import pandas as pd

from accumulator.config import ACC_DATASET_PATH, STATION_PARAMETERS, MODELS_TO_RUN
from accumulator.models.chill import calculate_chill_hours
from accumulator.ncdf_utils import read_ncdf, write_ncdf, combine_datasets
from accumulator.parm import Parm
from accumulator.portal import fetch_parm


def set_time_stamp() -> int:
    """
    Calculate the number of hours since the reference date

    :return: Hours since reference date as int
    """
    current_time = datetime.now()
    reference_date = datetime(1990, 1, 1, 0, 0, 0)
    new_time_stamp = (current_time - reference_date).total_seconds() // 3600  # 3600 seconds in an hour
    return int(new_time_stamp)


def run_selected_models(models: list, combined_data: pd.DataFrame):
    updated_accumulation = combined_data
    if 'utah' in models:
        updated_accumulation = calculate_chill_hours(combined_data, 'utah')
    return updated_accumulation


def main():
    # Set the time stamp
    new_time_stamp = set_time_stamp()

    # Fetch the latest tair data from DataPortal at the top of the hour for each station
    parms = Parm(STATION_PARAMETERS)
    stations_csv = fetch_parm(parms)

    accumulator_ncdf = read_ncdf(ACC_DATASET_PATH)

    # Combine data from the DataPortal and NetCDF4 file into a pandas DataFrame
    combined_data = combine_datasets(stations_csv, accumulator_ncdf)

    # Calculate Chill Hours using the Utah Model
    updated_accumulation = run_selected_models(MODELS_TO_RUN, combined_data)

    # Save accumulated hours to NetCDF4 file
    write_ncdf(updated_accumulation, accumulator_ncdf, new_time_stamp)


if __name__ == '__main__':
    main()
