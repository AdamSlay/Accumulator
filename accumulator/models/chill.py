import logging
import pandas as pd

from accumulator.environment import CHILL_HOURS_VAR

logger = logging.getLogger(__name__)


def utah_model(tair: float, stid: str) -> float:
    """
    Calculate Chill Hours using the Utah Model (Richardson et al. 1974)

    Utah Model Accumulation Ranges:
            T <= 34.0F = 0.0
    34.0F < T <= 36.0F = 0.5
    36.0F < T <= 48.0F = 1.0
    48.0F < T <= 54.0F = 0.5
    54.0F < T <= 60.0F = 0.0
    60.0F < T <= 65.0F = -0.5
    65.0F < T          = -1.0

    :param tair: Air Temperature (F)
    :param stid: Station ID string for Warning
    :return: Total Accumulated Chill Hours
    """
    if tair <= 34.0:
        accumulated = 0.0

    elif 34.0 < tair <= 36.0:
        accumulated = 0.5

    elif 36.0 < tair <= 48.0:
        accumulated = 1.0

    elif 48.0 < tair <= 54.0:
        accumulated = 0.5

    elif 54.0 < tair <= 60.0:
        accumulated = 0.0

    elif 60.0 < tair <= 65.0:
        accumulated = -0.5

    elif 65.0 < tair < 999.0:
        accumulated = -1.0

    else:
        logger.warning(f"Invalid tair value for {stid}: {tair}")
        accumulated = 0.0

    return accumulated


def calculate_chill_hours(stations: pd.DataFrame) -> pd.DataFrame:
    """
    Iterate over the stations and calculate the chill hours for each

    :param stations: DataFrame of station data
    :return: DataFrame of station data with updated chill hours
    """

    # TODO: allow for different models to be used based on model config in Accumulator/etc/config/chill_hours.yaml
    model = 'utah'
    logger.debug(f"Calculating chill hours using {model} model")
    
    for index, station in stations.iterrows():
        try:
            tair = float(station['tair'])
            logger.debug(f"Calculating chill hours for {station.name}: {tair}")
        except ValueError:
            logger.error(f"Invalid temperature value for {station.name}: {station['tair']}")
            stations.loc[index, CHILL_HOURS_VAR] = 0.0
            continue
       
        # for now there is only the one model
        if model == 'utah':
            new_chill_hours = utah_model(tair, str(station.name))
            logger.debug(f"New chill hours for {station.name}: {new_chill_hours}. RUNNING UTAH MODEL")
        else:
            new_chill_hours = utah_model(tair, str(station.name))

        stations.loc[index, CHILL_HOURS_VAR] = new_chill_hours
        logger.debug(f"New chill hours for {station.name}: {new_chill_hours}")
    
    logger.debug("Finished calculating chill hours")
    return stations
