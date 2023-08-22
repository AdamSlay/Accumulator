from datetime import datetime
import netCDF4 as nc
import numpy as np
import pandas as pd

from accumulator.config import ACC_DATASET_PATH, CHILL_HOURS_VAR, MODELS_TO_RUN
from accumulator.models.chill import calculate_chill_hours


def set_time_stamp() -> int:
    """
    Calculate the number of hours since the reference date

    :return: Hours since reference date as int
    """
    current_time = datetime.now()
    reference_date = datetime(1990, 1, 1, 0, 0, 0)
    new_time_stamp = (current_time - reference_date).total_seconds() // 3600  # 3600 seconds in an hour
    return int(new_time_stamp)


def run_selected_models(combined_data: pd.DataFrame):
    """
    Run the selected models and return the updated accumulation

    :param combined_data: pd.DataFrame of combined datasets (DataPortal and NetCDF4)
    :return: pd.DataFrame of updated dataset
    """
    updated_accumulation = combined_data
    if 'utah' in MODELS_TO_RUN:
        updated_accumulation = calculate_chill_hours(combined_data, 'utah')
    return updated_accumulation


def write_ncdf(updated_accumulation: pd.DataFrame, new_time_stamp: int) -> None:
    """
    Write the total accumulated chill hours to the NetCDF4 file

    Note: the accumulated chill hours are never allowed to go below 0

    :param updated_accumulation: Total Accumulated Chill Hours
    :param new_time_stamp: New time stamp to be added
    """

    # Open the NetCDF4 file
    accumulator_ncdf = nc.Dataset(ACC_DATASET_PATH, 'a', format='NETCDF4')
    time_index = len(accumulator_ncdf.dimensions['time'])

    # Extract the existing values for CHILL_HOURS_VAR
    existing_chill_hours = accumulator_ncdf[CHILL_HOURS_VAR][time_index - 1, :]

    # Add the updated accumulation values, ensuring the result never goes below 0
    chill_hours_values = updated_accumulation[CHILL_HOURS_VAR].values
    new_chill_hours = np.maximum(existing_chill_hours + chill_hours_values, 0)

    accumulator_ncdf[CHILL_HOURS_VAR][time_index, :] = new_chill_hours
    accumulator_ncdf['time'][time_index] = new_time_stamp

    # Close the file
    accumulator_ncdf.close()
