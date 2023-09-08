import json
from unittest.mock import MagicMock
import pandas as pd

from accumulator.portal import convert_resp_to_df
from accumulator import portal


def test_fetch_station_data(monkeypatch):
    mock_socket = MagicMock()
    monkeypatch.setattr("socket.socket", lambda *args, **kwargs: mock_socket)

    mock_query = {"type": "test_type", "dataset": "test_dataset", "date": "test_date",
                  "variables": ["test_var1", "test_var2"]}
    monkeypatch.setattr(portal, "build_query", lambda: mock_query)

    mock_response = {"success": True, "response": {"test_var1": {"data": [1, 2, 3]}, "test_var2": {"data": [4, 5, 6]}}}
    monkeypatch.setattr(portal, "receive_response", lambda x: mock_response)

    mock_df = pd.DataFrame(mock_response['response'])
    monkeypatch.setattr(portal, "convert_resp_to_df", lambda x: mock_df)

    result = portal.fetch_station_data()

    pd.testing.assert_frame_equal(result, mock_df)


def test_build_query():
    result = portal.build_query("test_type", "test_dataset", "test_date", ["test_var1", "test_var2"])
    expected = {"type": "test_type",
                "dataset": "test_dataset",
                "date": "test_date",
                "variables": ["test_var1", "test_var2"]
                }

    assert result == expected


def test_receive_response(monkeypatch):
    mock_socket = MagicMock()
    monkeypatch.setattr("socket.socket", lambda *args, **kwargs: mock_socket)

    expected = {"success": True, "response": {"test_var1": {"data": [1, 2, 3]}, "test_var2": {"data": [4, 5, 6]}}}

    mock_socket.recv.return_value = json.dumps(expected).encode()

    # Mock the socket's recv method to return the expected response on the first call
    # and an empty bytes object on subsequent calls
    mock_socket.recv.side_effect = [json.dumps(expected).encode(), b'']
    
    result = portal.receive_response(mock_socket)
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
