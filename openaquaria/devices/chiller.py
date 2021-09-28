import threading
import time
import typing

import gpiozero

from openaquaria import units


class MatchState(threading.Thread):
    def __init__(
        self,
        pin_spec: int,
        control_func: typing.Callable[[], bool],
        interval_seconds: int = 30,
    ):
        super().__init__(daemon=True)
        self.control_pin = gpiozero.Device.pin_factory.pin(pin_spec)
        self.control_pin.output_with_state(0)
        self.state = 0
        self.control_func = control_func
        self.interval_seconds = interval_seconds

    def check_state(self):
        next_state = self.control_func()
        self.control_pin.state = next_state
        self.state = next_state

    def run(self):
        while True:
            self.check_state()
            time.sleep(self.interval_seconds)


class Chiller(MatchState):
    def __init__(
        self,
        control_pin: int,
        temp_reader: typing.Callable[[], units.Temperature],
        max_temp: units.Temperature,
        interval_seconds: int = 5,
    ):
        self.temp_reader = temp_reader
        self.max_temp = max_temp
        super().__init__(control_pin, self.__should_be_on, interval_seconds)

    def __should_be_on(self) -> bool:
        current_temp = self.temp_reader()
        if current_temp.celsius > self.max_temp.celsius:
            return True
        return False


class Heater(MatchState):
    def __init__(
        self,
        control_pin: int,
        temp_reader: typing.Callable[[], units.Temperature],
        min_temp: units.Temperature,
        interval_seconds: int = 5,
    ):
        self.temp_reader = temp_reader
        self.min_temp = min_temp
        super().__init__(control_pin, self.__should_be_on, interval_seconds)

    def __should_be_on(self) -> bool:
        current_temp = self.temp_reader()
        if current_temp.celsius < self.min_temp.celsius:
            return True
        return False
