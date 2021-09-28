import pytest

from openaquaria import units


def test_temperature():
    temp = units.Temperature(0)
    assert temp.fahrenheit == 32


def test_temperature_from_fahrenheit():
    temp = units.Temperature.from_fahrenheit(32)
    assert temp.celsius == 0


def test_temperature_from_string_no_units():
    with pytest.raises(ValueError):
        units.Temperature.from_string("12345")


def test_temperature_from_string_celsius():
    t = units.Temperature.from_string("100 C")

    assert t.celsius == 100.0


def test_temperature_from_string_fahrenheit():
    t = units.Temperature.from_string("50 F")

    assert t.celsius == 10
