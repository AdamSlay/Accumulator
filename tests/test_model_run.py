import pandas as pd
from unittest.mock import patch

from accumulator import config
from accumulator.model_run import run_models, MODEL_FUNCTIONS

# Test data
test_data = pd.DataFrame({
    'column1': [1, 2, 3],
    'column2': [4, 5, 6]
})


# Mocked model function
def mock_model_function(data):
    return data * 2


@patch.dict(MODEL_FUNCTIONS, {config.CHILL_HOURS_VAR: mock_model_function})
def test_run_models():
    result = run_models(test_data)
    pd.testing.assert_frame_equal(result, test_data * 2)
