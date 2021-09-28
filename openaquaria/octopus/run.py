import time
import threading
import typing

import uvicorn
from strictyaml import YAML

from openaquaria.devices.display import Display, TemperaturePage
from openaquaria.devices.thermometer import Thermometer
from openaquaria.octopus.sensor import SensorArray, Sensor
from openaquaria.octopus.observer import Observer
from openaquaria.config import load_config, Inhabitant, Species
from openaquaria.octopus.rest import Router, app
from openaquaria.inventory import Inventory, split_genus_species
from openaquaria.units import Temperature


def background_loop(stop_event: threading.Event, host: Host, inv: Inventory):
    while not stop_event.is_set():
        host.check()
        time.sleep(1)


def get_inhabiting_species(
    inhabitants: typing.List[Inhabitant],
    inv: Inventory,
):
    found_species: typing.List[str] = []

    for i in inhabitants:
        if i.species not in found_species:
            found_species.append(i.species.data)

    inhabitant_species = []

    for sp in found_species:
        split = split_genus_species(sp)
        inhabitant_species.append(inv.get_species(split[0], split[1]))

    return inhabitant_species


def get_min_max_temperature(
    inh: typing.List[Species],
) -> typing.Tuple[Temperature, Temperature]:
    minimum: typing.Optional[Temperature] = None
    maximum: typing.Optional[Temperature] = None

    for i in inh:
        if minimum is None or minimum.celsius < i.temperature.minimum.celsius:
            minimum = i.temperature.minimum

        if maximum is None or maximum.celsius > i.temperature.maximum.celsius:
            maximum = i.temperature.maximum

    if minimum is None:
        minimum = Temperature(0)

    if maximum is None:
        maximum = Temperature(100)
    return (minimum, maximum)


def run():
    conf = load_config("./docs/octopus.config.yml")
    stop_event = threading.Event()
    inv = Inventory(conf.genuses)

    inhabiting_species = get_inhabiting_species(conf.tanks[0].inhabitants, inv)
    min_max_temp = get_min_max_temperature(inhabiting_species)

    router = Router()
    sensor_array = SensorArray()

    display = None
    if conf.display is not None:
        display = Display(
            stop_event,
            conf.display.device,
            conf.display.address,
        )
        display.start()

    for t in conf.tanks:
        therm = Thermometer(t.thermometer.device, t.thermometer.pin)
        router.add_thermometer(therm)
        sens = Sensor(60, therm.read)
        sensor_array.add_sensor(sens)
        if display is not None:
            page = TemperaturePage(min_max_temp[0], min_max_temp[1])
            obs = Observer()
            obs.add_callback(page.set_temperature)
            display.add_page(page)

    sensor_array.start()
    app.get("/taxonomy")(lambda: inv.to_dict())
    app.get("/tank")(
        lambda: {
            "acceptable_temperatures": {
                "minimum": str(min_max_temp[0].fahrenheit) + " F",
                "maximum": str(min_max_temp[1].fahrenheit) + " F",
            }
        }
    )
    uvicorn.run(app, host="0.0.0.0", port=8000)

    # while True:
    #    h.check()
    #    time.sleep(1)


if __name__ == "__main__":
    run()
