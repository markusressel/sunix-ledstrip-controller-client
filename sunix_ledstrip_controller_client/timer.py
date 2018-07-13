from datetime import datetime
from enum import Enum


class Timer:
    """
    Representation of a single timer configuration
    """

    STATE_ENABLED = 0xf0
    STATE_DISABLED = 0x00

    def __init__(self, enabled: bool,
                 execution_time: datetime, pattern: any,
                 red: int, green: int, blue: int):
        self._enabled = enabled

        self._execution_time = execution_time
        self._execution_pattern = pattern

        self._red = red
        self._green = green
        self._blue = blue

    def __str__(self):
        return ("Enabled: %s\n" % (self.get_enabled()) +
                "Execution Time: %s\n" % (self.get_execution_time()) +
                "Execution Pattern: %s\n" % (self.get_execution_pattern()))

    def get_enabled(self):
        """
        :return: True if this timer is enabled
        """
        return self._enabled

    def get_execution_time(self):
        """
        :return: the time when this timer will execute
        """
        return self._execution_time

    def get_execution_pattern(self):
        """
        :return: the execution pattern for this timer
        """
        return self._execution_pattern


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
    """
    Constants for specific action modes of a timer
    """

    TurnOn = 0xf0
    TurnOff = 0x00
    Color = 0x61
