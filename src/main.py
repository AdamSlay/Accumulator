from src.models.chill import calculate_chill
from netcdf import read_ncdf, write_ncdf, combine_datasets
from portal import fetch_parm
from parm import Parm
from datetime import datetime


def main():
    # Calculate the number of hours since the reference date
    current_time = datetime.now()
    reference_date = datetime(2000, 1, 1, 0, 0, 0)
    new_time_stamp = (current_time - reference_date).total_seconds() / 3600

    # Define the parameters to fetch
    parms = Parm([('tair', "fahr")])  # this should be part of the config file

    # Fetch the latest tair data from DataPortal at the top of the hour for each station
    stations_csv = fetch_parm(parms)

    # Fetch the Accumulator NetCDF4 file
    accumulator_ncdf = read_ncdf('../data/ncdf/accumulator.nc')

    # Combine data from the DataPortal and NetCDF4 file into a pandas DataFrame
    combined_data = combine_datasets(stations_csv, accumulator_ncdf)

    # Calculate Chill Hours using the Utah Model
    updated_accumulation = calculate_chill(combined_data)

    # Save accumulated hours to NetCDF4 file
    write_ncdf(updated_accumulation, accumulator_ncdf, new_time_stamp)


if __name__ == '__main__':
    main()
