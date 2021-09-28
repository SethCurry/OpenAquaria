from __future__ import annotations
import typing

import requests
from jsonschema import validate


class Species:
    schema = {
        "type": "object",
        "properties": {
            "id": {"type": "number"},
            "name": {"type": "string"},
        },
    }

    def __init__(self, id: int, name: str):
        self.id = id
        self.name = name

    @staticmethod
    def from_dict(d: typing.Dict[str, typing.Any]) -> Species:
        validate(d, Species.schema)

        return Species(d["id"], d["name"])


class Client:
    def __init__(self, base_url: str):
        self.base_url = base_url

    def list_species(self) -> typing.List[Species]:
        resp = requests.get(self.base_url + "/v1/species")

        species = []

        for i in resp.json():
            species.append(Species.from_dict(i))

        return species
