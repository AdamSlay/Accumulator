import netCDF4 as nc
import numpy as np
import pandas as pd
from accumulator.config import CHILL_HOURS_VAR, ACC_DATASET_PATH


def chill_hours_update(existing_values: pd.DataFrame, updates: pd.DataFrame) -> pd.DataFrame:
    """
    Update the accumulated chill hours using the following rules:
        1. If the existing value + update is less than 0, set it to 0
        2. Otherwise, set it to the existing value + update

    :param existing_values: Existing value in the NetCDF4 file
    :param updates: The new values to be accumulated
    :return: The updated value
    """
    return np.maximum(existing_values + updates, 0)


# Function Map for updating the NetCDF4 file with each model
update_functions = {
    CHILL_HOURS_VAR: chill_hours_update
}


def write_ncdf(updated_accumulation: pd.DataFrame, new_time_stamp: int) -> None:
    """
    Iterate through the accumulated variables and apply the corresponding update function

    :param updated_accumulation: Total Accumulated Chill Hours
    :param new_time_stamp: New time stamp to be added to the NetCDF4 file
    """

    ncdf_dataset = nc.Dataset(ACC_DATASET_PATH, 'a', format='NETCDF4')
    time_index = len(ncdf_dataset.dimensions['time'])

    for var_name, update_function in update_functions.items():
        existing_values = ncdf_dataset[var_name][time_index - 1, :]
        updates = updated_accumulation[var_name].values
        new_values = update_function(existing_values, updates)
        ncdf_dataset[var_name][time_index, :] = new_values

    ncdf_dataset['time'][time_index] = new_time_stamp
    ncdf_dataset.close()
