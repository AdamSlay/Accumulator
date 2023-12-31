from datetime import datetime
import netCDF4 as nc
import numpy as np
import os
import pandas as pd

from accumulator import config, logger
from accumulator.utils.create_ncdf import create_dataset


def chill_hours_update_func(existing_values: pd.DataFrame, updates: pd.DataFrame) -> pd.DataFrame:
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
UPDATE_FUNCTIONS = {
    config.CHILL_HOURS_VAR: chill_hours_update_func
}


def set_time_stamp() -> int:
    """
    Calculate the number of hours since the reference date

    :return: Hours since reference date as int
    """
    current_time = datetime.now()
    reference_date = datetime(1990, 1, 1, 0, 0, 0)
    new_time_stamp = (current_time - reference_date).total_seconds() // 3600  # 3600 seconds in an hour

    logger.log.info(f"New time stamp: {new_time_stamp}")
    return int(new_time_stamp)


def route_var_to_update_func(dataset: nc.Dataset, var_name: str, updated_accumulation: pd.DataFrame, time_index: int):
    """
    Update the variable in the NetCDF4 file using the corresponding update function

    :param dataset: the NetCDF4 dataset
    :param var_name: the name of the variable to update
    :param updated_accumulation: the updated accumulation data as a DataFrame
    :param time_index: the index of the time dimension to update
    :return: None
    """
    try:
        existing_values = dataset[var_name][time_index - 1, :]
        updates = updated_accumulation[var_name].values
        update_function = UPDATE_FUNCTIONS[var_name]
        new_values = update_function(existing_values, updates)
        dataset[var_name][time_index, :] = new_values
    except KeyError as e:
        logger.log.error(f"Variable {var_name} not found in the dataset: {e}")
        raise
    except IndexError as e:
        logger.log.error(f"Index error occurred while accessing the data of {var_name}: {e}")
        raise
    except Exception as e:
        logger.log.error(f"Error occurred while updating the data of {var_name} in update_variable(): {e}")
        raise


def open_ncdf() -> nc.Dataset:
    """
    Open the NetCDF4 file specified by ACC_DATASET_PATH for writing

    :return: NetCDF4 dataset
    """

    if not os.path.isfile(config.ACCUM_DATASET_PATH):
        logger.log.warning(f"NetCDF4 file not found at {config.ACCUM_DATASET_PATH}")

        try:
            logger.log.info(f"Creating NetCDF4 file at {config.ACCUM_DATASET_PATH}")
            create_dataset(config.ACCUM_DATASET_PATH)
        except (PermissionError, OSError) as e:
            logger.log.error(f"An error occurred while creating the NetCDF4 file: {e}")
            raise

    try:
        ncdf_dataset = nc.Dataset(config.ACCUM_DATASET_PATH, 'a', format='NETCDF4')
    except PermissionError as e:
        logger.log.error(f"Permission denied for {config.ACCUM_DATASET_PATH}: {e}")
        raise
    except OSError as e:
        logger.log.error(f"OS error occurred while opening {config.ACCUM_DATASET_PATH}: {e}")
        raise

    return ncdf_dataset


def write_ncdf(updated_accumulation: pd.DataFrame, update_functions: dict[str, callable] = None) -> None:
    """
    Write the updated accumulation data to the NetCDF4 file
    :param updated_accumulation: The updated accumulation data as a DataFrame
    :param update_functions: A dictionary mapping variable names to update functions
    :return: None
    """
    logger.log.info(f"Writing data to NetCDF4 file: {config.ACCUM_DATASET_PATH}")

    if update_functions is None:
        update_functions = UPDATE_FUNCTIONS

    ncdf_dataset = None

    try:
        ncdf_dataset = open_ncdf()
        time_index = len(ncdf_dataset.dimensions['time'])
        update_ncdf_data(ncdf_dataset, updated_accumulation, time_index, update_functions)
    except (PermissionError, OSError, FileNotFoundError) as e:
        logger.log.error(f"An error occurred while writing to the NetCDF4 file: {e}")
        raise
    finally:
        if ncdf_dataset:
            ncdf_dataset.close()
            logger.log.info("Closing NetCDF4 file")


def update_ncdf_data(ncdf_dataset: nc.Dataset, updated_accumulation: pd.DataFrame, time_index: int, update_functions: dict[str, callable]) -> None:
    """
    Update the NetCDF4 file with the updated accumulation data
    :param ncdf_dataset: The NetCDF4 dataset
    :param updated_accumulation: The updated accumulation data as a DataFrame
    :param time_index: The index of the time dimension to update
    :param update_functions: A dictionary mapping variable names to update functions
    :return: None
    """
    ncdf_dataset['time'][time_index] = set_time_stamp()
    for i, (var_name, update_function) in enumerate(update_functions.items()):
        logger.log.info(f"Updating variable {i + 1} of {len(update_functions)}: {var_name}")
        route_var_to_update_func(ncdf_dataset, var_name, updated_accumulation, time_index)
