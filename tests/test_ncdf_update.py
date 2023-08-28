import pandas as pd
from unittest import mock

from accumulator.environment import ACCUM_DATASET_PATH
from accumulator.ncdf_update import chill_hours_update, open_ncdf, write_ncdf, check_dataset_exists, set_time_stamp, \
    update_variable


def test_chill_hours_update():
    existing_values = pd.DataFrame({'chill_hours': [10, 20, 30]})
    updates = pd.DataFrame({'chill_hours': [1.0, -1.0, 0.0]})

    result = chill_hours_update(existing_values, updates)

    expected_result = pd.DataFrame({'chill_hours': [11.0, 19.0, 30.0]})
    pd.testing.assert_frame_equal(result, expected_result)


@mock.patch('os.path.isfile')
def test_check_dataset_exists(mock_isfile):
    mock_isfile.return_value = True
    assert check_dataset_exists() is True

    mock_isfile.return_value = False
    assert check_dataset_exists() is False


def test_set_time_stamp():
    assert isinstance(set_time_stamp(), int)


@mock.patch('accumulator.ncdf_update.update_functions')
def test_update_variable(mock_update_functions):
    # Create a mock dataset with a mock variable
    mock_dataset = mock.MagicMock()
    mock_variable = mock.MagicMock()
    mock_dataset.__getitem__.return_value = mock_variable

    # Mock the update function to return the updates as is
    mock_update_function = mock.MagicMock(side_effect=lambda x, y: y)
    mock_update_functions.__getitem__.return_value = mock_update_function

    # Create test data
    var_name = 'test_var'
    updated_accumulation = pd.DataFrame({var_name: [1.0, -1.0, 0.0]})
    time_index = 1

    # Call the function
    existing_values = mock_variable[time_index - 1, :]
    existing_values_result = existing_values[:]
    update_variable(mock_dataset, var_name, updated_accumulation, time_index)

    # Check that the function interacted with the mock objects as expected
    mock_dataset.__getitem__.assert_any_call(var_name)
    mock_variable.__getitem__.assert_any_call((time_index - 1, slice(None, None, None)))
    mock_update_functions.__getitem__.assert_called_once_with(var_name)
    mock_update_function.assert_called_once_with(existing_values_result, updated_accumulation[var_name].values)


@mock.patch('os.path.isfile')
@mock.patch('netCDF4.Dataset')
def test_open_ncdf(mock_nc_dataset, mock_isfile):
    # Mock the return value of isfile to simulate the file existing
    mock_isfile.return_value = True
    mock_nc_dataset.return_value = 'mock dataset'

    result = open_ncdf()

    mock_nc_dataset.assert_called_once_with(ACCUM_DATASET_PATH, 'a', format='NETCDF4')
    assert result == 'mock dataset'


@mock.patch('accumulator.ncdf_update.open_ncdf')
@mock.patch('netCDF4.Dataset')
def test_write_ncdf(mock_nc_dataset, mock_open_ncdf):
    # Create a mock dataset
    mock_dataset = mock.MagicMock()
    mock_open_ncdf.return_value = mock_dataset

    station_data = {'tair': ['10', 'invalid', '35'], 'stid': ['station1', 'station2', 'station3']}
    stations = pd.DataFrame(station_data)

    write_ncdf(stations)

    assert mock_open_ncdf.call_count == 1
    assert mock_dataset.close.call_count == 1
