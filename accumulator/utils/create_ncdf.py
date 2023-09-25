import netCDF4 as nc
import numpy as np
import pandas as pd
from netCDF4 import date2num
from datetime import datetime, timedelta

from accumulator import config


def create_dataset(file_path=config.ACCUM_DATASET_PATH):
    # Define the path and create the file
    csv_file_path = 'accumulator/utils/latest_tair.csv'
    df = pd.read_csv(csv_file_path)
    station_ids = df['stid'].values.tolist()  # Extract the station IDs

    nc_file = nc.Dataset(file_path, mode='w', format='NETCDF4')

    try:
        # Define dimensions
        nc_file.createDimension('time', None)  # Unlimited dimension
        nc_file.createDimension('station', 120)
        nc_file.createDimension('string_length', 4)  # Character dimension for station_ids

        # Define variables
        variables = ["chill_hours"]
        for var in variables:
            var = nc_file.createVariable(var, "f4", ("time", "station"))
            var.units = 'hours'
            var.description = f'Accumulated {var} per station'

        # Write station_ids to the file
        station_id_var = nc_file.createVariable('station_id', 'S1', ('station', 'string_length'))  # String variable
        for i, station_id in enumerate(station_ids):
            station_id_var[i, :] = list(station_id.ljust(4))  # Left-justify to ensure fixed length

        # Initialize the first time entry with the most recent top of the hour
        now = datetime.now()
        start_time = now.replace(minute=0, second=0, microsecond=0)  # Set minutes, seconds, and microseconds to zero
        if now.minute > 0:  # If it's past the top of the hour, move to the next hour
            start_time += timedelta(hours=1)
        time_var = nc_file.createVariable('time', np.int32, ('time',))
        time_var.units = 'hours since 1990-01-01 00:00:00'
        time_var.calendar = 'gregorian'
        time_var[0] = date2num(start_time, units=time_var.units, calendar=time_var.calendar)

        # Initialize accumulated variables with zeros
        for var in variables:
            var = nc_file.variables[var]
            var[0, :] = 0.0

    finally:
        # Ensure the file is closed even if an error occurs
        nc_file.close()
