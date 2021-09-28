from enum import Enum


class PeltierState(Enum):
    OFF = 0
    COOLING = 1
    HEATING = 2


class Peltier:
    def __init__(self):
        pass

    def set_state(self, state: PeltierState):
        return
