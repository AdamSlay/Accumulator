from accumulator.models.chill import calculate_chill_hours
from datetime import datetime
import pandas as pd


def set_time_stamp() -> int:
    """
    Calculate the number of hours since the reference date

    :return: Hours since reference date as int
    """
    current_time = datetime.now()
    reference_date = datetime(1990, 1, 1, 0, 0, 0)
    new_time_stamp = (current_time - reference_date).total_seconds() // 3600  # 3600 seconds in an hour
    return int(new_time_stamp)


def run_selected_models(models: list, combined_data: pd.DataFrame):
    """
    Run the selected models and return the updated accumulation

    :param models: list of models to run
    :param combined_data: pd.DataFrame of combined datasets (DataPortal and NetCDF4)
    :return: pd.DataFrame of updated dataset
    """
    updated_accumulation = combined_data
    if 'utah' in models:
        updated_accumulation = calculate_chill_hours(combined_data, 'utah')
    return updated_accumulation

