import pytest

from openaquaria import config


def test_TemperatureRange_missing_minimum():
    with pytest.raises(KeyError, match="'minimum'"):
        config.TemperatureRange.from_dict({"maximum": "12 F"})
