from datetime import datetime


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
