def meters_to_miles(meters: float) -> float:
    """
    Converts meters to miles.

    :param meters: The distance in meters.
    :return: The distance in miles.
    """
    return meters * 0.000621371


def meters_to_feet(meters: float) -> float:
    """
    Converts meters to feet.

    :param meters: The distance in meters.
    :return: The distance in feet.
    """
    return meters * 3.28084


def ms_to_mph(meters_per_second: float) -> float:
    """
    Converts meters per second to miles per hour.

    :param meters_per_second: The speed in meters per second.
    :return: The speed in miles per hour.
    """
    return meters_per_second * 2.23694


def c_to_f(celsius: float) -> float:
    """
    Converts Celsius to Fahrenheit.

    :param celsius: The temperature in Celsius.
    :return: The temperature in Fahrenheit.
    """
    return (celsius * 9 / 5) + 32
