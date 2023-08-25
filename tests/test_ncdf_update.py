import pandas as pd
from unittest import mock

from accumulator.config import ACC_DATASET_PATH
from accumulator.ncdf_update import chill_hours_update, open_ncdf, write_ncdf


def test_chill_hours_update():
    existing_values = pd.DataFrame({'chill_hours': [10, 20, 30]})
    updates = pd.DataFrame({'chill_hours': [1.0, -1.0, 0.0]})

    result = chill_hours_update(existing_values, updates)

    expected_result = pd.DataFrame({'chill_hours': [11.0, 19.0, 30.0]})
    pd.testing.assert_frame_equal(result, expected_result)


@mock.patch('netCDF4.Dataset')
def test_open_ncdf(mock_nc_dataset):
    mock_nc_dataset.return_value = 'mock dataset'

    result = open_ncdf()

    mock_nc_dataset.assert_called_once_with(ACC_DATASET_PATH, 'a', format='NETCDF4')
    assert result == 'mock dataset'


@mock.patch('netCDF4.Dataset')
def test_write_ncdf(mock_nc_dataset):
    # Create a mock dataset
    mock_dataset = mock.MagicMock()
    mock_nc_dataset.return_value = mock_dataset

    # Create a DataFrame with test data
    station_data = {'tair': ['10', 'invalid', '35'], 'stid': ['station1', 'station2', 'station3']}
    stations = pd.DataFrame(station_data)

    # Call the function
    write_ncdf(stations)

    # Check that the function interacted with the mock dataset as expected
    assert mock_nc_dataset.call_count == 1
    assert mock_nc_dataset.call_args[0][0] == ACC_DATASET_PATH
    assert mock_nc_dataset.call_args[0][1] == 'a'
    assert mock_dataset.close.call_count == 1
