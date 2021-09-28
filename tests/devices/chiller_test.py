from gpiozero import Device
from gpiozero.pins.mock import MockFactory
from openaquaria.devices import chiller
from openaquaria.units import Temperature

Device.pin_factory = MockFactory()


def test_chiller():
    def inner_reader() -> Temperature:
        return Temperature(40)

    c = chiller.Chiller(1, inner_reader, Temperature(10))
    c.check_state()
    assert c.state == 1
