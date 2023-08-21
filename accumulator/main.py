from accumulator.config import ACC_DATASET_PATH, STATION_PARAMETERS
from accumulator.ncdf_utils import read_ncdf, write_ncdf, combine_datasets
from accumulator.parm import Parm
from accumulator.portal import fetch_parm
from accumulator.utils import set_time_stamp, run_selected_models


def main():
    # Set the time stamp
    new_time_stamp = set_time_stamp()

    # Fetch the latest tair data from DataPortal at the top of the hour for each station
    parms = Parm(STATION_PARAMETERS)
    stations_csv = fetch_parm(parms)

    accumulator_ncdf = read_ncdf(ACC_DATASET_PATH)

    # Combine data from the DataPortal and NetCDF4 file into a pandas DataFrame
    combined_data = combine_datasets(stations_csv, accumulator_ncdf)

    # Calculate Chill Hours using the Utah Model
    updated_accumulation = run_selected_models(combined_data)

    # Save accumulated hours to NetCDF4 file
    write_ncdf(updated_accumulation, accumulator_ncdf, new_time_stamp)


if __name__ == '__main__':
    main()
