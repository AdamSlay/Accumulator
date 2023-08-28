import pandas as pd
import numpy as np
import netCDF4 as nc
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


def test_update_variable():
    # Create a test NetCDF4 file in diskless mode so that it doesn't actually write to disk
    dataset = nc.Dataset('/tmp/test.nc', 'w', diskless=True)
    dataset.createDimension('time', None)
    dataset.createDimension('station', 3)
    var = dataset.createVariable('chill_hours', np.float32, ('time', 'station'))
    var[0, :] = np.array([1.0, 2.0, 3.0])

    # Create a test DataFrame
    updated_accumulation = pd.DataFrame({'chill_hours': [1.0, -1.0, 0.0]})

    # Call the function
    update_variable(dataset, 'chill_hours', updated_accumulation, 1)
    expected_values = np.array([2.0, 1.0, 3.0])

    assert np.all(dataset['chill_hours'][1, :] == expected_values)


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

    station_data = {'chill_hours': ['10', 'invalid', '35'], 'stid': ['station1', 'station2', 'station3']}
    stations = pd.DataFrame(station_data)
    write_ncdf(stations)

    assert mock_open_ncdf.call_count == 1
    assert mock_dataset.close.call_count == 1
