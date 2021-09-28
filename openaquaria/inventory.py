import typing
import enum

from openaquaria.config import Species, Genus


class GenusFamily(enum.Enum):
    FISH = "Fish"
    AMPHIBIAN = "Amphibian"
    MOSS = "Moss"
    PLANT = "Plant"
    SNAIL = "Snail"
    SHRIMP = "Shrimp"


def split_genus_species(s: str) -> typing.Tuple[str, str]:
    parts = s.split(" ")
    if len(parts) != 2:
        raise ValueError("invalid number of spaces")
    return (parts[0], parts[1])


class Inventory:
    def __init__(self, genuses: typing.Dict[str, Genus]):
        self.genuses: typing.Dict[str, Genus] = genuses

    def add_species(self, genus: str, sp: Species):
        self.genuses[genus].species[sp.name] = sp

    def get_species(self, genus: str, sp: str):
        return self.genuses[genus].species[sp]

    def to_dict(self) -> typing.Dict[str, typing.Any]:
        return {g.name: g.to_dict() for g in self.genuses.values()}
