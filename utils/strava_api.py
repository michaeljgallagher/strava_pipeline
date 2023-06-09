from datetime import datetime
from itertools import count
from time import sleep

import requests


def get_access_token(client_id, client_secret, refresh_token):
    """
    Retrieves the access token from Strava API using the provided client ID, client secret, and refresh token.

    :param client_id: The client ID.
    :type client_id: str
    :param client_secret: The client secret.
    :type client_secret: str
    :param refresh_token: The refresh token.
    :type refresh_token: str
    :return: The access token.
    :rtype: str
    :raises RuntimeError: If there is an error retrieving the access token.
    """
    payload = {
        "client_id": client_id,
        "client_secret": client_secret,
        "refresh_token": refresh_token,
        "grant_type": "refresh_token",
        "f": "json",
    }
    res = requests.post("https://www.strava.com/oauth/token", data=payload)
    if res.status_code == 200:
        return res.json()["access_token"]
    else:
        raise RuntimeError(res.text)


def get_activities(access_token, start_date):
    """
    Retrieves the activities from Strava API starting from the specified date.

    :param access_token: The access token.
    :type access_token: str
    :param start_date: The start date in UNIX timestamp format.
    :type start_date: int
    :return: The list of activities.
    :rtype: list
    :raises RuntimeError: If there is an error retrieving the activities.
    """
    activities = []
    url = "https://www.strava.com/api/v3/athlete/activities"
    headers = {"Authorization": "Bearer " + access_token}
    params = {
        "after": start_date,
        "per_page": 30,
        "page": 1,
    }
    for i in count(1):
        if i % 81 == 0:
            print("API limit reached, sleeping for 15 minutes")
            sleep(15 * 60)
        params["page"] = i
        res = requests.get(url, headers=headers, params=params)
        if res.status_code == 200:
            cur = res.json()
            if len(cur) == 0:
                break
            activities += cur
        else:
            raise RuntimeError(res.text)
    return activities


def get_start_date(activity):
    """
    Retrieves the start date of an activity.

    :param activity: The activity data.
    :type activity: dict
    :return: The start date in UNIX timestamp format.
    :rtype: int
    """
    start_date = activity["start_date"]
    return int(datetime.fromisoformat(start_date).timestamp())
