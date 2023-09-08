import json
from unittest.mock import MagicMock
import pandas as pd

from accumulator.portal import convert_resp_to_df
from accumulator import portal


def test_fetch_station_data(monkeypatch):
    # Mock the socket connection
    mock_socket = MagicMock()
    monkeypatch.setattr("socket.socket", lambda *args, **kwargs: mock_socket)

    # Mock the query
    mock_query = {"type": "test_type", "dataset": "test_dataset", "date": "test_date",
                  "variables": ["test_var1", "test_var2"]}
    monkeypatch.setattr(portal, "build_query", lambda: mock_query)

    # Mock the response
    mock_response = {"success": True, "response": {"test_var1": {"data": [1, 2, 3]}, "test_var2": {"data": [4, 5, 6]}}}
    monkeypatch.setattr(portal, "receive_response", lambda x: mock_response)

    # Mock the DataFrame conversion
    mock_df = pd.DataFrame(mock_response['response'])
    monkeypatch.setattr(portal, "convert_resp_to_df", lambda x: mock_df)

    # Call the function
    result = portal.fetch_station_data()

    # Assert the result
    pd.testing.assert_frame_equal(result, mock_df)


def test_build_query():
    # Call the function with some test inputs
    result = portal.build_query("test_type", "test_dataset", "test_date", ["test_var1", "test_var2"])

    # Define the expected result
    expected = {"type": "test_type",
                "dataset": "test_dataset",
                "date": "test_date",
                "variables": ["test_var1", "test_var2"]
                }

    # Assert that the result matches the expected result
    assert result == expected


def test_receive_response(monkeypatch):
    # Mock the socket connection
    mock_socket = MagicMock()
    monkeypatch.setattr("socket.socket", lambda *args, **kwargs: mock_socket)

    # Define the expected response
    expected = {"success": True, "response": {"test_var1": {"data": [1, 2, 3]}, "test_var2": {"data": [4, 5, 6]}}}

    # Mock the socket's recv method to return the expected response
    mock_socket.recv.return_value = json.dumps(expected).encode()
    # Mock the socket's recv method to return the expected response on the first call and an empty bytes object on subsequent calls
    mock_socket.recv.side_effect = [json.dumps(expected).encode(), b'']
    
    # Call the function
    result = portal.receive_response(mock_socket)

    # Assert that the result matches the expected result
    assert result == expected


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
