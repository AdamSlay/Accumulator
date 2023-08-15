import netCDF4 as nc
import pandas as pd


def read_ncdf():
    """
    Read the NetCDF4 file and return the accumulated chill hours
    """


def write_ncdf(total_accumulation: float, accumulated_chill: nc.Dataset):
    """
    Write the total accumulated chill hours to the NetCDF4 file

    :param total_accumulation: Total Accumulated Chill Hours
    :param accumulated_chill: NetCDF4 file
    """


def combine_data(station_tair: list, accumulated_chill: nc.Dataset) -> pd.DataFrame:
    """
    Combine the DataPortal data and the NetCDF4 data and return as pandas DataFrame

    :param station_tair: DataPortal data
    :param accumulated_chill: NetCDF4 data
    :return: Combined data as pandas DataFrame
    """
    return pd.DataFrame()