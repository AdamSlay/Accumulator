import pandas as pd
from unittest.mock import patch
from accumulator.model_run import run_models, MODEL_FUNCTIONS
from accumulator.environment import CHILL_HOURS_VAR

# Test data
test_data = pd.DataFrame({
    'column1': [1, 2, 3],
    'column2': [4, 5, 6]
})


# Mocked model function
def mock_model_function(data):
    return data * 2


@patch.dict(MODEL_FUNCTIONS, {CHILL_HOURS_VAR: mock_model_function})
def test_run_models():
    result = run_models(test_data)
    pd.testing.assert_frame_equal(result, test_data * 2)
