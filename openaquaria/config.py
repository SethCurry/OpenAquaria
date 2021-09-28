from __future__ import annotations

import typing
from strictyaml import Map, Int, Str, Seq, load, MapPattern, YAML

from openaquaria.units import TemperatureRange


class Species:
    schema = Map(
        {
            "common_name": Str(),
            "temperature": TemperatureRange.schema,
        }
    )

    def __init__(
        self,
        name: str,
        common_name: str,
        temperature: TemperatureRange,
    ):
        self.name = name
        self.common_name = common_name
        self.temperature = temperature

    @staticmethod
    def from_dict(name: str, d: typing.Dict[str, YAML]):
        return Species(
            name,
            d["common_name"].data,
            TemperatureRange.from_dict(d["temperature"]),
        )

    def to_dict(self) -> typing.Dict[str, typing.Any]:
        return {
            "name": self.name,
            "common_name": self.common_name,
            "temperature": self.temperature.to_dict(),
        }


class Thermometer:
    schema = Map({"device": Str(), "pin": Int()})

    def __init__(self, device: YAML, pin: YAML):
        self.device = device
        self.pin = pin

    @staticmethod
    def from_dict(d: typing.Dict[str, YAML]) -> Thermometer:
        device = ""
        pin = 0

        if "device" in d:
            device = d["device"]
        else:
            raise KeyError('missing key "device"')

        if "pin" in d:
            pin = d["pin"]
        else:
            raise KeyError('missing key "pin"')
        return Thermometer(device, pin)


class Inhabitant:
    schema = Map({"name": Str(), "species": Str()})

    def __init__(self, name: str, species: str):
        self.name = name
        self.species = species

    @staticmethod
    def from_dict(d: typing.Dict[str, YAML]) -> Inhabitant:
        return Inhabitant(d["name"].data, d["species"].data)


class Tank:
    schema = Map(
        {
            "name": Str(),
            "thermometer": Thermometer.schema,
            "inhabitants": Seq(Inhabitant.schema),
        }
    )

    def __init__(
        self,
        name: str,
        thermometer: typing.Optional[Thermometer],
        inhabitants: typing.List[Inhabitant],
    ):
        self.name = name
        self.thermometer = thermometer
        self.inhabitants = inhabitants

    @staticmethod
    def from_dict(d: typing.Dict[str, YAML]) -> Tank:
        name = ""
        thermometer = None
        if "name" in d:
            name = d["name"].data
        else:
            raise KeyError('missing key "name"')

        if "thermometer" in d:
            thermometer = Thermometer.from_dict(d["thermometer"])

        inhabitants = [Inhabitant.from_dict(x) for x in d["inhabitants"]]

        return Tank(name, thermometer, inhabitants)


class Display:
    schema = Map({"device": Str(), "address": Str()})

    def __init__(self, device: str, address: str):
        """Create a new Display.

        Args:
            device (str): The model of the display
            address (str): The I2C address of the display in hex
        """
        self.device = device
        self.address = int(address, 16)

    @staticmethod
    def from_dict(d: typing.Dict[str, YAML]) -> Display:
        device = ""
        address = ""
        if "device" in d:
            device = d["device"].data
        else:
            raise KeyError('missing key "device"')

        if "address" in d:
            address = d["address"].data
        else:
            raise KeyError('missing key "address')

        return Display(device, address)


class Genus:
    schema = Map(
        {
            "family": Str(),
            "species": MapPattern(Str(), Species.schema),
        }
    )

    def __init__(
        self,
        name: str,
        family: str,
        species: typing.Dict[str, Species],
    ):
        self.name = name
        self.family = family
        self.species = species

    @staticmethod
    def from_dict(name: str, d: typing.Dict[str, YAML]):
        species = {}

        for s in d["species"]:
            species[s] = Species.from_dict(s.data, d["species"][s])
        return Genus(name, d["family"].data, species)

    def to_dict(self) -> typing.Dict[str, typing.Any]:
        return {
            "name": self.name,
            "family": self.family,
            "species": {s.name: s.to_dict() for s in self.species.values()},
        }


class Camera:
    schema = Map(
        {
            "interval": Str(),
            "dir": Str(),
        }
    )


class Config:
    schema = Map(
        {
            "display": Display.schema,
            "tanks": Seq(Tank.schema),
            "genuses": MapPattern(Str(), Genus.schema),
        }
    )

    def __init__(
        self,
        display: typing.Optional[Display],
        tanks: typing.Optional[typing.List[Tank]],
        genuses: typing.Optional[typing.Dict[str, Genus]],
    ):
        self.display = display
        self.tanks = tanks
        self.genuses = genuses

    @staticmethod
    def from_dict(d: typing.Dict[str, typing.Any]) -> Config:
        display = None
        if "display" in d:
            display = Display.from_dict(d["display"])

        tanks = None
        if "tanks" in d:
            tanks = []
            for t in d["tanks"]:
                tanks.append(Tank.from_dict(t))

        genuses = None
        if "genuses" in d:
            genuses = {}
            for g in d["genuses"]:
                genuses[g] = Genus.from_dict(g.data, d["genuses"][g])
        return Config(display, tanks, genuses)


def load_config(config_path: str) -> Config:
    with open(config_path) as fd:
        contents = fd.read()

    loaded = load(contents, Config.schema)

    return Config.from_dict(loaded)
