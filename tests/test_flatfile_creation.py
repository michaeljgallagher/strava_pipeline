import os
import tempfile
from csv import DictReader

import pytest
from utils.flatfile import parse_activity, save_to_csv


def test_parse_activity():
    activity = {
        "distance": 5000,
        "total_elevation_gain": 1000,
        "elev_high": 300,
        "elev_low": 100,
        "average_speed": 2.5,
        "max_speed": 3.0,
        "average_temp": 20,
        "start_latlng": [37.123, -122.456],
        "end_latlng": [37.456, -122.789],
        "unknown_col": "some data",
    }

    # Test parsing all columns
    cols = list(activity.keys())
    expected_res = {
        "distance": pytest.approx(3.106856),
        "total_elevation_gain": pytest.approx(3280.839895),
        "elev_high": pytest.approx(984.251969),
        "elev_low": pytest.approx(328.0839895),
        "average_speed": pytest.approx(5.59235),
        "max_speed": pytest.approx(6.71082),
        "average_temp": pytest.approx(68.0),
        "start_lat": 37.123,
        "start_lng": -122.456,
        "end_lat": 37.456,
        "end_lng": -122.789,
        "unknown_col": "some data",
    }
    assert parse_activity(activity, cols) == expected_res

    # Test parsing subset of columns
    cols = ["distance", "total_elevation_gain"]
    expected_res = {
        "distance": pytest.approx(3.106856),
        "total_elevation_gain": pytest.approx(3280.839895),
    }
    assert parse_activity(activity, cols) == expected_res

    # Test parsing empty activity
    activity = {}
    cols = []
    assert parse_activity(activity, cols) == {}


def test_save_to_csv():
    temppath = tempfile.NamedTemporaryFile().name
    print(temppath)
    cols = [
        "distance",
        "total_elevation_gain",
        "elev_high",
        "elev_low",
        "average_speed",
        "max_speed",
        "average_temp",
        "start_latlng",
        "end_latlng",
    ]
    csv_cols = [
        "distance",
        "total_elevation_gain",
        "elev_high",
        "elev_low",
        "average_speed",
        "max_speed",
        "average_temp",
        "start_lat",
        "start_lng",
        "end_lat",
        "end_lng",
    ]
    activities = [
        {
            "distance": 5000,
            "total_elevation_gain": 1000,
            "elev_high": 300,
            "elev_low": 100,
            "average_speed": 2.5,
            "max_speed": 3.0,
            "average_temp": 20,
            "start_latlng": [37.123, -122.456],
            "end_latlng": [37.456, -122.789],
        },
        {
            "distance": 100,
            "total_elevation_gain": 200,
            "elev_high": 910,
            "elev_low": 101,
            "average_speed": 7.3,
            "max_speed": 3.8,
            "average_temp": 29,
            "start_latlng": [48.543, -128.256],
            "end_latlng": [-37.123, -64.99],
        },
    ]
    save_to_csv(activities, temppath, cols, csv_cols)
    with open(temppath) as f:
        reader = DictReader(f, delimiter="\u0001")
        header = reader.fieldnames
        rows = list(reader)
        print(rows)
    assert header == csv_cols
    assert len(rows) == 2
    expected_rows = [
        {
            "distance": "3.106855",
            "total_elevation_gain": "3280.84",
            "elev_high": "984.252",
            "elev_low": "328.084",
            "average_speed": "5.592350000000001",
            "max_speed": "6.71082",
            "average_temp": "68.0",
            "start_lat": "37.123",
            "start_lng": "-122.456",
            "end_lat": "37.456",
            "end_lng": "-122.789",
        },
        {
            "distance": "0.0621371",
            "total_elevation_gain": "656.168",
            "elev_high": "2985.5644",
            "elev_low": "331.36484",
            "average_speed": "16.329662",
            "max_speed": "8.500372",
            "average_temp": "84.2",
            "start_lat": "48.543",
            "start_lng": "-128.256",
            "end_lat": "-37.123",
            "end_lng": "-64.99",
        },
    ]
    assert rows == expected_rows
    os.remove(temppath)
