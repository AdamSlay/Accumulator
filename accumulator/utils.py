from datetime import datetime
import logging

import pandas as pd

from accumulator.config import MODELS_TO_RUN
from accumulator.models.chill import calculate_chill_hours

logger = logging.getLogger(__name__)


def set_time_stamp() -> int:
    """
    Calculate the number of hours since the reference date

    :return: Hours since reference date as int
    """
    current_time = datetime.now()
    reference_date = datetime(1990, 1, 1, 0, 0, 0)
    new_time_stamp = (current_time - reference_date).total_seconds() // 3600  # 3600 seconds in an hour
    return int(new_time_stamp)


def run_models(combined_data: pd.DataFrame):
    """
    Run the selected models and return the updated accumulation

    New models added to the application will need to be implemented here

    :param combined_data: pd.DataFrame of combined datasets (DataPortal and NetCDF4)
    :return: pd.DataFrame of updated dataset
    """
    updated_accumulation = combined_data
    for model in MODELS_TO_RUN:
        try:
            if model == 'utah':
                updated_accumulation = calculate_chill_hours(combined_data, 'utah')
            if model == 'grape_rot':
                pass  # example of a model that has not been implemented yet
        except Exception as e:
            logger.error(f"Failed to run model {model} with error {e}")

    return updated_accumulation
