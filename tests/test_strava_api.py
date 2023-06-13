from datetime import datetime

import pytest
import requests_mock
from utils.strava_api import get_access_token, get_activities, get_start_date


@pytest.fixture
def mock_requests():
    with requests_mock.Mocker() as m:
        yield m


def test_get_access_token_success(mock_requests):
    client_id = "client_id"
    client_secret = "client_secret"
    refresh_token = "refresh_token"
    access_token = "access_token"
    payload = {
        "access_token": access_token,
        "expires_at": 1623383464,
        "expires_in": 21600,
        "refresh_token": refresh_token,
        "token_type": "Bearer",
        "athlete": {"id": 12345678, "username": "testuser"},
    }
    mock_requests.post(
        "https://www.strava.com/oauth/token",
        json=payload,
        status_code=200,
    )

    result = get_access_token(client_id, client_secret, refresh_token)
    assert result == access_token


def test_get_access_token_failure(mock_requests):
    client_id = "client_id"
    client_secret = "client_secret"
    refresh_token = "refresh_token"
    error_message = "Invalid refresh token"
    mock_requests.post(
        "https://www.strava.com/oauth/token",
        text=error_message,
        status_code=400,
    )
    with pytest.raises(RuntimeError) as excinfo:
        get_access_token(client_id, client_secret, refresh_token)
    assert str(excinfo.value) == error_message


def test_get_activities_success(mock_requests):
    access_token = "access_token"
    start_date = 1623336000
    activities = [{"id": 1, "name": "Activity 1"}, {"id": 2, "name": "Activity 2"}]

    # Mock the API response for the first page
    mock_requests.get(
        "https://www.strava.com/api/v3/athlete/activities?page=1",
        json=activities,
        status_code=200,
    )

    # Mock the API response for the second page
    mock_requests.get(
        "https://www.strava.com/api/v3/athlete/activities?page=2",
        json=[],
        status_code=200,
    )

    result = get_activities(access_token, start_date)
    expected_result = activities
    assert result == expected_result


def test_get_activities_failure(mock_requests):
    access_token = "your_access_token"
    start_date = 1623336000
    error_message = "Invalid access token"
    mock_requests.get(
        "https://www.strava.com/api/v3/athlete/activities",
        text=error_message,
        status_code=401,
    )
    with pytest.raises(RuntimeError) as excinfo:
        get_activities(access_token, start_date)
    assert str(excinfo.value) == error_message


def test_get_start_date():
    activity = {
        "id": 1,
        "name": "Activity 1",
        "start_date": "2023-06-01T12:00:00Z",
    }
    expected_start_date = int(
        datetime.fromisoformat("2023-06-01T12:00:00Z").timestamp()
    )
    result = get_start_date(activity)
    assert result == expected_start_date
