import os
from csv import DictWriter
from typing import Dict, List, Union

from strava_pipeline.utils.conversions import (
    c_to_f,
    meters_to_feet,
    meters_to_miles,
    ms_to_mph,
)


def parse_activity(
    activity: Dict[str, Union[int, float, List[float]]], cols: List[str]
) -> Dict[str, Union[int, float, str]]:
    """
    Parses the activity data and applies the appropriate conversions based on the column name.

    :param activity: The activity data.
    :param cols: The list of columns to parse.
    :return: The parsed activity data.
    """
    res = {}
    for col in cols:
        cur = activity.get(col, None)
        if cur is None:
            res[col] = None
            continue
        match col:
            case "distance":
                res[col] = meters_to_miles(cur)
            case "total_elevation_gain" | "elev_high" | "elev_low":
                res[col] = meters_to_feet(cur)
            case "average_speed" | "max_speed":
                res[col] = ms_to_mph(cur)
            case "average_temp":
                res[col] = c_to_f(cur)
            case _ if col.endswith("_latlng"):
                pfix = col.split("_")[0]
                if cur == []:
                    cur = [None, None]
                res[pfix + "_lat"] = cur[0]
                res[pfix + "_lng"] = cur[1]
            case _:
                res[col] = cur
    return res


def save_to_csv(
    activities: List[Dict[str, Union[int, float, List[float]]]],
    csv_path: str,
    cols: List[str],
    csv_cols: List[str],
) -> None:
    """
    Saves the activity data to a CSV file.

    :param activities: The list of activity data.
    :param csv_path: The path to the CSV file.
    :param cols: The list of columns to include.
    :param csv_cols: The corresponding CSV column names.
    """
    os.makedirs(os.path.dirname(csv_path), exist_ok=True)
    with open(csv_path, "w") as f:
        writer = DictWriter(f, fieldnames=csv_cols, delimiter="\u0001")
        writer.writeheader()
        for activity in activities:
            writer.writerow(parse_activity(activity, cols))
