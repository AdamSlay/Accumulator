from datetime import datetime
import logging
import netCDF4 as nc
import numpy as np
import os
import pandas as pd

from accumulator.environment import ACCUM_DATASET_PATH, CHILL_HOURS_VAR

log = logging.getLogger(__name__)


def chill_hours_update(existing_values: pd.DataFrame, updates: pd.DataFrame) -> pd.DataFrame:
    """
    Update the accumulated chill hours using the following rules:
        1. If the existing value + update is less than 0, set it to 0
        2. Otherwise, set it to the existing value + update

    :param existing_values: Existing value in the NetCDF4 file
    :param updates: The new values to be accumulated
    :return: The updated value
    """
    return np.maximum(existing_values + updates, 0.0)


# Function Map for updating the NetCDF4 file with each model
update_functions = {
    CHILL_HOURS_VAR: chill_hours_update
}


def check_dataset_exists() -> bool:
    """
    Check if the NetCDF4 dataset exists

    :return: True if the dataset exists, False otherwise
    """
    return os.path.isfile(ACCUM_DATASET_PATH)


def set_time_stamp() -> int:
    """
    Calculate the number of hours since the reference date

    :return: Hours since reference date as int
    """
    current_time = datetime.now()
    reference_date = datetime(1990, 1, 1, 0, 0, 0)
    new_time_stamp = (current_time - reference_date).total_seconds() // 3600  # 3600 seconds in an hour

    log.info(f"New time stamp: {new_time_stamp}")
    return int(new_time_stamp)


def update_variable(dataset: nc.Dataset, var_name: str, updated_accumulation: pd.DataFrame, time_index: int):
    try:
        existing_values = dataset[var_name][var_name][time_index - 1, :]
        updates = updated_accumulation[var_name].values
        update_function = update_functions[var_name]
        new_values = update_function(existing_values, updates)
        dataset[var_name][var_name][time_index, :] = new_values
    except KeyError:
        log.error(f"Variable {var_name} not found in the dataset")
    except IndexError:
        log.error(f"Index error occurred while accessing the data of {var_name}")


def open_ncdf() -> nc.Dataset:
    """
    Open the NetCDF4 file specified by ACC_DATASET_PATH for writing
    """
    
    if not check_dataset_exists():
        print(f"File not found: {ACCUM_DATASET_PATH}")
        raise FileNotFoundError(f"File not found: {ACCUM_DATASET_PATH}")
    
    try:
        ncdf_dataset = nc.Dataset(ACCUM_DATASET_PATH, 'a', format='NETCDF4')
    except PermissionError:
        raise RuntimeError(f"Permission denied: {ACCUM_DATASET_PATH}")
    except OSError as e:
        raise RuntimeError(f"OS error occurred while opening the file: {e}")
    return ncdf_dataset


def write_ncdf(updated_accumulation: pd.DataFrame) -> None:
    """
    Iterate through the accumulated variables and apply the corresponding update function

    :param updated_accumulation: Total Accumulated Chill Hours
    """
    log.info(f"Writing data to NetCDF4 file: {ACCUM_DATASET_PATH}")

    try:
        ncdf_dataset = open_ncdf()
    except RuntimeError or FileNotFoundError as e:
        log.error(e)
        return

    time_index = len(ncdf_dataset.dimensions['time'])  # len of time dimension = next index to append to

    for i, (var_name, update_function) in enumerate(update_functions.items()):
        log.info(f"Updating variable {i + 1} of {len(update_functions)}: {var_name}")
        update_variable(ncdf_dataset, var_name, updated_accumulation, time_index)

    ncdf_dataset['time'][time_index] = set_time_stamp()
    ncdf_dataset.close()
    log.info("Closing NetCDF4 file")
