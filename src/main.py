from chill import utah_model
from portal import fetch_parm


def main():
    # Fetch the latest tair data from DataPortal at the top of the hour for each station
    # Fetch the latest accumulated chill hours from the NetCDF4 file for each station
    # Calculate Chill Hours using the Utah Model
    # Add the result to the accumulated chill hours
    # Save accumulated hours to NetCDF4 file
    return


if __name__ == '__main__':
    main()
