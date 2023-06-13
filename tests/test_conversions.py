import pytest
from utils.conversions import c_to_f, meters_to_feet, meters_to_miles, ms_to_mph


def test_meters_to_miles():
    assert meters_to_miles(0) == 0
    assert meters_to_miles(1609.344) == pytest.approx(1)
    assert meters_to_miles(-1609.344) == pytest.approx(-1)


def test_meters_to_feet():
    assert meters_to_feet(0) == 0
    assert meters_to_feet(1) == pytest.approx(3.28084)
    assert meters_to_feet(-1) == pytest.approx(-3.28084)


def test_ms_to_mph():
    assert ms_to_mph(0) == 0
    assert ms_to_mph(1) == pytest.approx(2.23694)
    assert ms_to_mph(-1) == pytest.approx(-2.23694)


def test_c_to_f():
    assert c_to_f(0) == 32
    assert c_to_f(100) == pytest.approx(212)
    assert c_to_f(-40) == pytest.approx(-40)
