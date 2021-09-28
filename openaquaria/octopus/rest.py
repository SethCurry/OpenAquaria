import typing
from fastapi import FastAPI

from openaquaria.devices.thermometer import Thermometer

app = FastAPI()


class Router:
    def __init__(self):
        self.thermometers: typing.List[Thermometer] = []

    def add_thermometer(self, th: Thermometer):
        self.thermometers.append(th)

    @app.get("/thermometers")
    def find_thermometer(self):
        readings = []
        for i in self.thermometers:
            readings.append(i.read())
        return readings
