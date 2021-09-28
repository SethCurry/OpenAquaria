import abc
import threading
import time
import typing

from RPLCD.i2c import CharLCD
from openaquaria.devices.thermometer import Thermometer
from openaquaria.units import Temperature


class Page(abc.ABC):
    def __init__(self):
        return

    @abc.abstractmethod
    def render(self) -> str:
        return ""


class TemperaturePage(Page):
    def __init__(
        self,
        minimum: Temperature,
        maximum: Temperature,
    ):
        """A page for showing current and ideal temperatures.

        Args:
            thermometer (Thermometer): The thermometer to read
            minimum (Temperature): The minimum allowable temperature
            maximum (Temperature): The maximum allowable temperature

        """
        super().__init__()
        self.current_temperature = 0.0
        self.minimum = minimum
        self.maximum = maximum

    def render(self) -> str:
        min_temp = int(self.minimum.fahrenheit)
        max_temp = int(self.maximum.fahrenheit)
        return (
            f"Temp: {int(self.current_temperature)} F\n\rIdeal: {min_temp}-{max_temp} F"
        )

    def set_temperature(self, val: float):
        self.current_temperature = val


class PageManager:
    def __init__(self):
        self.pages: typing.List[Page] = []
        self.index = 0

    def add_page(self, page: Page):
        self.pages.append(page)

    def render(self) -> str:
        return self.pages[self.index].render()

    def next(self):
        if self.index + 1 >= len(self.pages):
            self.index = 0
        else:
            self.index += 1


# 16x2
class Display(threading.Thread):
    def __init__(self, stop_event: threading.Event, device: str, addr: int):
        super().__init__(daemon=True)
        self.lcd = CharLCD(device, addr)
        self.pages = PageManager()
        self.page_index = 0
        self.stop_event = stop_event

    def add_page(self, page: Page):
        self.pages.add_page(page)

    def run(self):
        while not self.stop_event.is_set():
            self.pages.next()
            rendered = self.pages.render()
            self.lcd.clear()
            self.lcd.write_string(rendered)
            time.sleep(5)
