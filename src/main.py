from src.models.chill import calculate_chill
from netcdf import read_ncdf, write_ncdf, combine_datasets
from portal import fetch_parm
from parm import Parm


def main():

    parms = Parm([('tair', "fahr"), ('wspd', 'mph')])  # this should be part of the config file

    # Fetch the latest tair data from DataPortal at the top of the hour for each station
    stations_csv = fetch_parm(parms)

    # Fetch the Accumulator NetCDF4 file
    accumulator_ncdf = read_ncdf()

    # Combine data from the DataPortal and NetCDF4 file into a pandas DataFrame
    combined_data = combine_datasets(stations_csv, accumulator_ncdf)

    # Calculate Chill Hours using the Utah Model
    updated_accumulation = calculate_chill(combined_data)

    # Save accumulated hours to NetCDF4 file
    write_ncdf(updated_accumulation, accumulator_ncdf)


if __name__ == '__main__':
    main()
