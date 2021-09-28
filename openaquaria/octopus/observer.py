import typing

Callback = typing.Callable[[float], None]


class Observer:
    def __init__(self):
        self._callbacks: typing.List[Callback] = []

    def add_callback(self, c: Callback):
        self._callbacks.append(c)


class Range(Observer):
    def __init__(self, minimum: float, maximum: float):
        super().__init__()
        self.minimum = minimum
        self.maximum = maximum

    def ingest(self, reading: float):
        if reading < self.minimum or reading > self.maximum:
            for i in self._callbacks:
                i(reading)
