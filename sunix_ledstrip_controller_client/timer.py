from datetime import datetime
from enum import Enum


class Timer:
    """
    Representation of a single timer configuration
    """

    def __init__(self, enabled: bool,
                 execution_time: datetime, pattern: any,
                 red: int, green: int, blue: int):
        self.enabled = enabled

        self.execution_time = execution_time
        self.execution_pattern = pattern

        self.red = red
        self.green = green
        self.blue = blue

    def __str__(self):
        # TODO
        return super().__str__()

    def get_time(self):
        return self.execution_time


class Weekday(Enum):
    """
    Constants that represent specific days for repeating timers
    """

    Mo = 0x02
    Tu = 0x04
    We = 0x08
    Th = 0x10
    Fr = 0x20
    Sa = 0x40
    Su = 0x80
    Everyday = Mo | Tu | We | Th | Fr | Sa | Su
    Weekdays = Mo | Tu | We | Th | Fr
    Weekend = Sa | Su


class Mode(Enum):
    TurnOn = 0xf0
    TurnOff = 0x00
    Color = 0x61
