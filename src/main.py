from chill import calculate_chill
from netcdf import read_ncdf, write_ncdf, combine_data
from portal import fetch_parm


def main():
    # Fetch the latest tair data from DataPortal at the top of the hour for each station
    station_tair = fetch_parm('tair')

    # Fetch the Accumulator NetCDF4 file
    accumulated_chill = read_ncdf()

    # Combine data from the DataPortal and NetCDF4 file into a pandas DataFrame
    combined_data = combine_data(station_tair, accumulated_chill)

    # Calculate Chill Hours using the Utah Model
    total_accumulation = calculate_chill(combined_data)

    # Save accumulated hours to NetCDF4 fil
    write_ncdf(total_accumulation, accumulated_chill)


if __name__ == '__main__':
    main()
