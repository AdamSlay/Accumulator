from accumulator.config import STATION_PARAMETERS
from accumulator.parm import Parm
from accumulator.portal import fetch_parm
from accumulator.utils import set_time_stamp, run_selected_models, write_ncdf


def main():
    # Set the time stamp
    new_time_stamp = set_time_stamp()

    # Fetch the latest tair data from DataPortal at the top of the hour for each station
    parms = Parm(STATION_PARAMETERS)
    stations_csv = fetch_parm(parms)

    # Run the models
    updated_accumulation = run_selected_models(stations_csv)

    # Save accumulated hours to NetCDF4 file
    write_ncdf(updated_accumulation, new_time_stamp)


if __name__ == '__main__':
    main()
