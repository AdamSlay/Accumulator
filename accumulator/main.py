from accumulator.ncdf_update import write_ncdf
from accumulator.portal import fetch_parm
from accumulator.utils import set_time_stamp, run_models


def main():
    # Fetch the latest tair data from DataPortal at the top of the hour for each station
    stations_csv = fetch_parm()

    # Run the models
    updated_accumulation = run_models(stations_csv)

    # Set time stamp and Save accumulated hours to NetCDF4 file
    new_time_stamp = set_time_stamp()
    write_ncdf(updated_accumulation, new_time_stamp)


if __name__ == '__main__':
    main()
