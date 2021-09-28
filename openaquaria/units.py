from __future__ import annotations
import typing
from strictyaml import Map, Str


class Temperature:
    def __init__(self, celcius: float):
        self.celsius = celcius

    @staticmethod
    def from_fahrenheit(fahr: float) -> Temperature:
        """Create a new Temperature from a Fahrenheit measurement.

        Args:
            fahr (float): The temperature in Fahrenheit

        Returns:
            A Temperature object at the provided temperature."""

        return Temperature((fahr - 32) * 5 / 9)

    @staticmethod
    def from_string(s: str) -> Temperature:
        """Parse a string into a temperature.

        Requires the string to end in either F or C,
        however it will parse both with and without
        a space between the numbers and the units.

        Args:
            s (str): The string to parse into a temperature

        Returns:
            A Temperature object parsed from the string."""

        final_char = s[-1].upper()
        num = float(s[:-1].strip())

        if final_char == "F":
            return Temperature.from_fahrenheit(num)
        elif final_char == "C":
            return Temperature(num)
        else:
            raise ValueError("temperature does not end with F or C")

    @property
    def fahrenheit(self):
        """float: The temperature in Fahrenheit"""

        return self.celsius * 1.8 + 32


class TemperatureRange:
    schema = Map({"minimum": Str(), "maximum": Str()})

    def __init__(self, minimum: Temperature, maximum: Temperature):
        self.minimum = minimum
        self.maximum = maximum

    def in_range(self, cmp: Temperature) -> bool:
        """Check whether the provided temperature is inside the range.

        Args:
            cmp (Temperature): The Temperature to compare
        """
        return cmp.celsius > self.minimum.celsius and cmp.celsius < self.maximum.celsius

    @staticmethod
    def from_dict(d: typing.Dict[str, typing.Any]) -> TemperatureRange:
        return TemperatureRange(
            Temperature.from_string(d["minimum"]),
            Temperature.from_string(d["maximum"]),
        )

    def to_dict(self) -> typing.Dict[str, typing.Any]:
        return {
            "minimum": str(self.minimum.fahrenheit) + " F",
            "maximum": str(self.maximum.fahrenheit) + " F",
        }


class Distance:
    def __init__(self, mm: float):
        self.mm = mm

    @property
    def inches(self) -> float:
        return self.mm / 25.4

    @property
    def meters(self) -> float:
        return self.mm / 100.0

    @staticmethod
    def from_inches(inch: float):
        return Distance(inch * 25.4)


class Volume:
    def __init__(self, meters: float):
        self.meters = meters

    def feet_cubed(self) -> float:
        return self.meters * 35.3147


class Dimensions:
    def __init__(self, length: Distance, width: Distance, height: Distance):
        self.length = length
        self.width = width
        self.height = height

    def volume(self) -> Volume:
        return Volume(self.length.meters * self.width.meters * self.height.meters)
