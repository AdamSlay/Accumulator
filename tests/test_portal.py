import io
import pandas as pd

from unittest import mock
from accumulator.portal import fetch_station_data


@mock.patch('pandas.read_csv')
@mock.patch('requests.get')
def test_fetch_parm(mock_get, mock_read_csv):
    # Create a mock response
    mock_response = mock.MagicMock()
    mock_response.content.decode.return_value = 'test_content'
    mock_get.return_value = mock_response

    # Create a mock DataFrame
    mock_df = pd.DataFrame()
    mock_read_csv.return_value = mock_df

    # Call the function
    result = fetch_station_data()

    # Check that the function interacted with the mocks as expected
    assert mock_get.call_count == 1
    assert mock_response.content.decode.call_count == 1
    assert mock_read_csv.call_count == 1
    assert isinstance(mock_read_csv.call_args[0][0], io.StringIO)

    # Check that the function returned the mock DataFrame
    pd.testing.assert_frame_equal(result, mock_df)
