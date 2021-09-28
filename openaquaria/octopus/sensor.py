from openaquaria.octopus.observer import Observer
import threading
import time
import typing

"""
sensors -> observer -> event -> listener

sensors create raw data
observer decides whether that raw data is worth an even
event carries info on what changed
listener does something with that information
"""

SensorCallback = typing.Callable[[float], None]
SensorReadFunc = typing.Callable[[], float]


class Sensor:
    def __init__(self, update_interval: int, reader: SensorReadFunc):
        self.__observers: typing.List[Observer] = []
        self.update_interval = update_interval
        self.reader = reader
        self.last_updated = 0
        self.last_reading = 0.0

    def read(self):
        self.last_reading = self.reader()

        for i in self.__observers:
            i.ingest(self.last_reading)

    def add_observer(self, obs: Observer):
        self.__observers.append(obs)


class SensorArray(threading.Thread):
    def __init__(self):
        super().__init__(daemon=True)
        self.__sensors: typing.List[Sensor] = []
        return

    def check(self):
        for i in self.__sensors:
            ct = time.time()
            if i.last_updated + i.update_interval < ct:
                i.read()

    def run(self):
        while True:
            self.check()

    def add_sensor(self, sen: Sensor):
        self.__sensors.append(sen)


"""
arr = SensorArray()
therm = Thermometer()
sensor = Sensor(15, therm.read)
arr.add_sensor(sensor)

obs = RangeObserver(70.0,80.0)

sensor.add_observer(obs)
"""
