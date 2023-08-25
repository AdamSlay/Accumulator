import logging
import pandas as pd

from accumulator.environment import MODELS_TO_RUN
from accumulator.models.chill import calculate_chill_hours

log = logging.getLogger(__name__)


MODEL_FUNCTIONS = {
    'chill_hours': calculate_chill_hours
}


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
            model_function = MODEL_FUNCTIONS.get(model)
            if model_function:
                updated_accumulation = model_function(combined_data)
            else:
                log.error(f"Model \"{model}\" not found")
        except Exception as e:
            log.error(f"Failed to run model {model}: {e}")

    log.info("Finished running models")
    return updated_accumulation