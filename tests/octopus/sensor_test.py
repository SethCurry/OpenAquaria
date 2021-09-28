from openaquaria.octopus.observer import Range
from openaquaria.octopus.sensor import Sensor

mut = 0.0


def test_Range_ingest():
    r = Range(10, 50)

    def handler(val: float):
        global mut
        mut = val

    r = Range(10, 50)
    r.add_callback(handler)

    def reading() -> float:
        return 8.2

    sensor = Sensor(15, reading)

    sensor.add_observer(r)
    sensor.read()

    assert mut == 8.2
