import pandas as pd
import pytest

from accumulator import config
from accumulator.models.chill import calculate_chill_hours, utah_model


@pytest.mark.parametrize("input_temp,expected_output", [
    (33.0, 0.0),  # freezing
    (34.0, 0.0),  # freezing
    (35.0, 0.5),  # cold
    (36.0, 0.5),  # cold
    (37.0, 1.0),  # chill
    (48.0, 1.0),  # chill
    (49.0, 0.5),  # cool
    (54.0, 0.5),  # cool
    (55.0, 0.0),  # neutral
    (60.0, 0.0),  # neutral
    (61.0, -0.5),  # warm
    (65.0, -0.5),  # warm
    (66.0, -1.0),  # hot
    (67.0, -1.0),  # hot
    (35.3, 0.5),  # decimal
    (36.7, 1.0)  # decimal
])
def test_utah_model(input_temp, expected_output):
    assert utah_model(input_temp, 'nrmn') == expected_output


def test_calculate_chill_hours():
    # Create a DataFrame with test data
    station_data = {'tair': [10.0, 'invalid', 35.0, 67.0], 'stid': ['station1', 'station2', 'station3', 'station4']}
    stations = pd.DataFrame(station_data)

    # Call the function
    result = calculate_chill_hours(stations)

    # Check that the returned DataFrame has the expected structure
    assert config.CHILL_HOURS_VAR in result.columns
    assert len(result) == len(stations)

    # Check that the returned DataFrame has the expected values
    assert result[config.CHILL_HOURS_VAR].iloc[0] == 0.0  # 10 degrees should result in 0.0 chill hours
    assert result[config.CHILL_HOURS_VAR].iloc[1] == 0.0  # 'invalid' temperature should result in 0.0 chill hours
    assert result[config.CHILL_HOURS_VAR].iloc[2] == 0.5  # 35 degrees should result in 0.5 chill hours
    assert result[config.CHILL_HOURS_VAR].iloc[3] == -1.0  # 67 degrees should result in -1.0 chill hours
