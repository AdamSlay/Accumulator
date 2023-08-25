import logging
import pandas as pd

from accumulator.config import MODELS_TO_RUN
from accumulator.models.chill import calculate_chill_hours

log = logging.getLogger(__name__)


def run_models(combined_data: pd.DataFrame):
    """
    Run the selected models and return the updated accumulation

    New models added to the application will need to be implemented here

    :param combined_data: pd.DataFrame of combined datasets (DataPortal and NetCDF4)
    :return: pd.DataFrame of updated dataset
    """
    updated_accumulation = combined_data
    for i, model in enumerate(MODELS_TO_RUN):
        log.info(f"Running model {i + 1} of {len(MODELS_TO_RUN)}: {model}")
        try:
            if model == 'utah':
                updated_accumulation = calculate_chill_hours(combined_data, 'utah')
            if model == 'grape_rot':
                pass  # example of a model that has not been implemented yet
        except Exception as e:
            log.error(f"Failed to run model {model}: {e}")

    log.info("Finished running models")
    return updated_accumulation
