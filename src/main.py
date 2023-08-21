from datetime import datetime

from netcdf import read_ncdf, write_ncdf, combine_datasets
from parm import Parm
from portal import fetch_parm
from src.models.chill import calculate_chill_hours


def set_time_stamp():
    # Calculate the number of hours since the reference date
    current_time = datetime.now()
    reference_date = datetime(1990, 1, 1, 0, 0, 0)
    new_time_stamp = (current_time - reference_date).total_seconds() / 3600  # 3600 seconds in an hour
    return new_time_stamp


def main():
    # Set the time stamp
    new_time_stamp = set_time_stamp()

    # Fetch the latest tair data from DataPortal at the top of the hour for each station
    # TODO: define parms based on the models specified in the config file
    parms = Parm([('tair', "fahr")])
    stations_csv = fetch_parm(parms)

    # TODO: use the config file to define the NetCDF4 file path
    accumulator_ncdf = read_ncdf('../data/ncdf/accumulator.nc')

    # Combine data from the DataPortal and NetCDF4 file into a pandas DataFrame
    combined_data = combine_datasets(stations_csv, accumulator_ncdf)

    # Calculate Chill Hours using the Utah Model
    # TODO: run all models specified in the config file
    updated_accumulation = calculate_chill_hours(combined_data)

    # Save accumulated hours to NetCDF4 file
    write_ncdf(updated_accumulation, accumulator_ncdf, new_time_stamp)


if __name__ == '__main__':
    main()
