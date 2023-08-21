import pandas as pd
import netCDF4 as nc

from accumulator.config import CHILL_HOURS_VAR


def read_ncdf(path: str) -> nc.Dataset:
    """
    Read the NetCDF4 file and return the dataset
    :param path: Path to the NetCDF4 file
    :return: NetCDF4 dataset
    """
    return nc.Dataset(path, 'a', format='NETCDF4')


def write_ncdf(updated_accumulation: pd.DataFrame, accumulator_ncdf: nc.Dataset, new_time_stamp: int) -> None:
    """
    Write the total accumulated chill hours to the NetCDF4 file
    :param updated_accumulation: Total Accumulated Chill Hours
    :param accumulator_ncdf: Accumulator NetCDF4 file
    :param new_time_stamp: New time stamp to be added
    """
    # Write the total accumulated chill hours to the NetCDF4 file at the new time stamp
    time_index = len(accumulator_ncdf.dimensions['time'])
    # TODO: make 'accumulated_chill' a parameter in the config file so it can be changed easily
    accumulator_ncdf[CHILL_HOURS_VAR][time_index, :] = updated_accumulation[CHILL_HOURS_VAR].values
    accumulator_ncdf['time'][time_index] = new_time_stamp

    # Close the file
    accumulator_ncdf.close()


def combine_datasets(station_data: pd.DataFrame, accumulated_chill: nc.Dataset) -> pd.DataFrame:
    """
    Combine the DataPortal data and the NetCDF4 data and return as pandas DataFrame

    :param station_data: DataPortal data
    :param accumulated_chill: NetCDF4 data
    :return: Combined data as pandas DataFrame
    """
    # Extract the 'stid' variable from the NetCDF4 data
    # Fetch the last value for each station
    stids = [''.join(s.tostring().decode('utf-8')) for s in accumulated_chill['station_id']]
    chill_values = [accumulated_chill[CHILL_HOURS_VAR][-1, i] for i in range(len(stids))]

    # Create a DataFrame from the NetCDF4 data
    ncdf_df = pd.DataFrame({
        'stid': stids,
        CHILL_HOURS_VAR: chill_values
    })

    # Merge the new ncdf_df and the station_data df
    combined_data = pd.merge(station_data, ncdf_df, on='stid')

    return combined_data
