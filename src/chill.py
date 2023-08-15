# Calculate Chill Hours using the Utah Model
import pandas as pd


def utah_model(tair: float, accumulated: float) -> float:
    """
    Calculate Chill Hours using the Utah Model (Richardson et al. 1974)

    Utah Model Accumulation Ranges:
    T <= 34.0F = 0.0
    34.0F < T <= 36.0F = 0.5
    36.0F < T <= 48.0F = 1.0
    48.0F < T <= 54.0F = 0.5
    54.0F < T <= 60.0F = 0.0
    60.0F < T <= 65.0F = -0.5
    65.0F < T = -1.0

    Note: total accumulated hours cannot be negative

    :param tair: Air Temperature (F)
    :param accumulated: Previously Accumulated Chill Hours
    :return: Total Accumulated Chill Hours
    """
    if tair <= 34.0:
        accumulated += 0.0

    elif 34.0 < tair <= 36.0:
        accumulated += 0.5

    elif 36.0 < tair <= 48.0:
        accumulated += 1.0

    elif 48.0 < tair <= 54.0:
        accumulated += 0.5

    elif 54.0 < tair <= 60.0:
        accumulated += 0.0

    elif 60.0 < tair <= 65.0:
        accumulated += -0.5

    elif tair > 65.0:
        accumulated += -1.0

    return accumulated if accumulated > 0.0 else 0.0


def calculate_chill(stations: pd.DataFrame):
    for station in stations:
        tair = float(station['tair'])
        accumulated_chill = float(station['accumulated_chill'])
        station['accumulated_chill'] = utah_model(tair, accumulated_chill)
