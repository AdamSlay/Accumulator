from unittest import mock

import pandas as pd

from accumulator.portal import fetch_station_data, convert_resp_to_df


@mock.patch('socket.socket')
def test_fetch_station_data(mock_socket):
    mock_socket_instance = mock.MagicMock()
    mock_socket.return_value = mock_socket_instance
    mock_socket_instance.recv.side_effect = [
        b'{"success": true, "response": {"stid": {"data": ["acme", "adax"]}, "relh": {"data": [26.1726, 25.8055]}, '
        b'"tair": {"data": [103.298, 104.828]}}}',
        b'']  # The empty string simulates the socket closing

    # Check that the function interacted with the mock socket as expected
    result = fetch_station_data()
    assert mock_socket.call_count == 1
    assert mock_socket_instance.connect.call_count == 1
    assert mock_socket_instance.sendall.call_count == 1
    assert mock_socket_instance.recv.call_count == 2  # Once for the response, once for the empty string

    expected_df = pd.DataFrame(
        {
            "stid": ["acme", "adax"],
            "relh": [26.1726, 25.8055],
            "tair": [103.298, 104.828]
        }
    )
    expected_df = expected_df.set_index('stid')
    pd.testing.assert_frame_equal(result, expected_df)


def test_convert_resp_to_df():
    mock_response = {"success": True,
                     "response": {"stid": {"data": ["acme", "adax"]},
                                  "relh": {"data": [26.1726, 25.8055]},
                                  "tair": {"data": [103.298, 104.828]}
                                  }
                     }

    expected_df = pd.DataFrame(
        {
            "stid": ["acme", "adax"],
            "relh": [26.1726, 25.8055],
            "tair": [103.298, 104.828]
        }
    )
    expected_df = expected_df.set_index('stid')

    result = convert_resp_to_df(mock_response)
    pd.testing.assert_frame_equal(result, expected_df)
