def meters_to_miles(meters):
    """
    Converts meters to miles.

    :param meters: The distance in meters.
    :type meters: float
    :return: The distance in miles.
    :rtype: float
    """
    return meters * 0.000621371


def meters_to_feet(meters):
    """
    Converts meters to feet.

    :param meters: The distance in meters.
    :type meters: float
    :return: The distance in feet.
    :rtype: float
    """
    return meters * 3.28084


def ms_to_mph(meters_per_second):
    """
    Converts meters per second to miles per hour.

    :param meters_per_second: The speed in meters per second.
    :type meters_per_second: float
    :return: The speed in miles per hour.
    :rtype: float
    """
    return meters_per_second * 2.23694


def c_to_f(celsius):
    """
    Converts Celsius to Fahrenheit.

    :param celsius: The temperature in Celsius.
    :type celsius: float
    :return: The temperature in Fahrenheit.
    :rtype: float
    """
    return (celsius * 9 / 5) + 32
