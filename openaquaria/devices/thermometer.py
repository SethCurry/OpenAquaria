import glob
import time

from prometheus_client import Gauge
from openaquaria.units import Temperature

TEMPER_GAUGE = Gauge("temperature", "Temperature of the tank in degrees.")


class Thermometer:
    def __init__(self):
        base_dir = "/sys/bus/w1/devices/"
        device_folder = glob.glob(base_dir + "28*")[0]
        self.device_file = device_folder + "/w1_slave"

    def __read_raw(self):
        with open(self.device_file, "r") as f:
            lines = f.readlines()
        return lines

    def read(self) -> Temperature:
        lines = self.__read_raw()

        while lines[0].strip()[-3:] != "YES":
            time.sleep(0.2)
            lines = self.__read_raw()

        equals_pos = lines[1].find("t=")
        if equals_pos != -1:
            temp_string = lines[1][equals_pos + 2 :]
            temp_c = float(temp_string) / 1000.0
            temp = Temperature(temp_c)
            TEMPER_GAUGE.set(temp.fahrenheit)
            return Temperature(temp_c)
        raise Exception("failed to read temperature")
