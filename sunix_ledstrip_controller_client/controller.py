import datetime

from sunix_ledstrip_controller_client.timer import Timer


class Controller:
    """
    Device class that represents a single controller
    """

    import datetime

    # workaround for cyclic dependencies introduced by typing
    from typing import TYPE_CHECKING
    if TYPE_CHECKING:
        from .client import LEDStripControllerClient

    from .functions import FunctionId
    from .packets import TransitionType

    POWER_STATE_ON = 0x23
    POWER_STATE_OFF = 0x24

    DEFAULT_PORT = 5577

    def __init__(self, api: 'LEDStripControllerClient', host: str, port: int = DEFAULT_PORT,
                 hardware_id: str = None, model: str = None):
        """
        Creates a new controller device object
        
        :param host: host address of the controller device
        :param port: the port on which the controller device is listening
        """

        self._api = api
        self._host = host
        if not port:
            self._port = self.DEFAULT_PORT
        else:
            self._port = port

        self._device_name = None
        self._hardware_id = hardware_id
        self._model = model

        self._power_state = None
        self._rgbww = None
        self._function = None
        self._function_speed = 255

        self.update_state()

    def __str__(self):
        return ("Host: %s\n" % (self.get_host()) +
                "Port: %s\n" % (self.get_port()) +
                "Device name: %s\n" % (self.get_device_name()) +
                "Hardware ID: %s\n" % (self.get_hardware_id()) +
                "Model: %s" % (self.get_model()))

    def get_host(self) -> str or None:
        """
        :return: The IP/Host address of this device  
        """
        return self._host

    def get_port(self) -> int:
        """
        :return: The port of this device 
        """
        return self._port

    def get_device_name(self) -> str or None:
        """
        :return: The device name of this controller
        """
        return self._device_name

    def get_hardware_id(self) -> str or None:
        """
        :return: The hardware ID of this device (f.ex. 'F0FE6B2333C6') 
        """
        return self._hardware_id

    def get_model(self) -> str or None:
        """
        :return: The model of this device 
        """
        return self._model

    def get_time(self) -> datetime:
        """
        :return: the current time of this controller
        """
        response = self._api.get_time(self._host, self._port)

        if (response["year"] is 0
                and response["month"] is 0
                and response["day"] is 0
                and response["hour"] is 0
                and response["minute"] is 0
                and response["second"] is 0):
            return None
        else:
            dt = datetime.datetime(
                response["year"] + 2000,
                response["month"],
                response["day"],
                response["hour"],
                response["minute"],
                response["second"]
            )
            return dt

    def set_time(self, date_time: datetime) -> None:
        """
        Sets the internal time of this controller

        :param date_time: the time to set
        """
        self._api.set_time(self._host, self._port, date_time)

    def is_on(self) -> bool:
        """
        :return: True if the controller is turned on, false otherwise
        """
        return self._power_state is self.POWER_STATE_ON

    def turn_on(self) -> None:
        """
        Turn on this controller
        """
        self._api.turn_on(self._host, self._port)
        self.update_state()

    def turn_off(self) -> None:
        """
        Turn on this controller
        """
        self._api.turn_off(self._host, self._port)
        self.update_state()

    def get_rgbww(self) -> (int, int, int, int, int) or None:
        """
        :return: the RGB color values
        """
        return self._rgbww

    def set_rgbww(self, red: int, green: int, blue: int,
                  warm_white: int, cold_white: int) -> None:
        """
        Sets rgbww values for this controller.

        :param red: red intensity (0..255)
        :param green: green intensity (0..255)
        :param blue: blue intensity (0..255)
        :param warm_white: warm_white: warm white intensity (0..255)
        :param cold_white: cold white intensity (0..255)
        """
        self._api.set_rgbww(self._host, self._port, red, green, blue, warm_white, cold_white)
        self.update_state()

    def set_rgb(self, red: int, green: int, blue: int) -> None:
        """
        Sets rgbw values for this controller.

        :param red: red intensity (0..255)
        :param green: green intensity (0..255)
        :param blue: blue intensity (0..255)
        """
        self._api.set_rgb(self._host, self._port, red, green, blue)
        self.update_state()

    def set_ww(self, warm_white: int, cold_white: int) -> None:
        """
        Sets warm white and cold white values for this controller.

        :param warm_white: warm white intensity (0..255)
        :param cold_white: cold white intensity (0..255)
        """
        self._api.set_ww(self._host, self._port, cold_white, warm_white)
        self.update_state()

    def get_brightness(self) -> int or None:
        """
        Note: this value is calculated in the library and not on the device
        :return: the brightness of the controller [0..255] or None if no value is set
        """
        if not self._rgbww:
            return None

        brightness = 0
        for color in self._rgbww:
            brightness += color

        return int(brightness / len(self._rgbww))

    def set_brightness(self, brightness: int) -> None:
        """
        Sets a specific brightness without changing the color.

        :param brightness: (0..255)
        """

        new_rgbww = []
        for color in self._rgbww:
            new_rgbww.append(color * (brightness / 255))

        self.set_rgbww(new_rgbww[0], new_rgbww[1], new_rgbww[2], new_rgbww[3], new_rgbww[4])

    def set_function(self, function_id: FunctionId, speed: int):
        """
        Sets a function on the specified controller

        :param function_id: Function ID
        :param speed: function speed [0..255] 0 is slow, 255 is fast
        """
        self._api.set_function(self._host, self._port, function_id, speed)
        self.update_state()

    def set_custom_function(self, color_values: [(int, int, int, int)],
                            speed: int, transition_type: TransitionType = TransitionType.Gradual):

        """
        Sets a custom function on this controller

        :param color_values: a list of up to 16 color tuples of the form
                             (red, green, blue) or
                             (red, green, blue, unknown).
                             I couldn't figure out what the last parameter is used for so the rgb is a shortcut.
        :param transition_type: the transition type between colors
        :param speed: function speed [0..255] 0 is slow, 255 is fast
        """
        self._api.set_custom_function(self._host, self._port, color_values, speed, transition_type)
        self.update_state()

    def get_timers(self) -> [Timer]:
        """
        Gets the defined timers of this controller

        :return: list of timers
        """

        def extract_timer_time(data: dict, idx: int) -> datetime:
            # combination of constants
            dayofweek = data["dayofweek_%d" % idx]
            if dayofweek != 0:
                return None

            year = data["year_%d" % idx] + 2000
            month = data["month_%d" % idx]
            day = data["day_%d" % idx]
            hour = data["hour_%d" % idx]
            minute = data["minute_%d" % idx]
            second = data["second_%d" % idx]

            execution_time = datetime.datetime.now().replace(day=day, month=month, year=year,
                                                             hour=hour, minute=minute, second=second)

            return execution_time

        def extract_timer_pattern(data: dict, idx: int) -> datetime:
            mode = data["action_code_%d" % idx]

            if (mode == 0x61):
                pass

            # TODO
            return mode

        timers_data = self._api.get_timers(self._host, self._port)

        timers = []
        for idx in range(1, 7):
            enabled = Timer.STATE_ENABLED == timers_data["is_active_%d" % idx]

            time = extract_timer_time(timers_data, idx)
            pattern = extract_timer_pattern(timers_data, idx)

            red = timers_data["red_%d" % idx]
            green = timers_data["green_%d" % idx]
            blue = timers_data["blue_%d" % idx]

            timer = Timer(
                enabled=enabled,
                execution_time=time,
                pattern=pattern,
                red=red,
                green=green,
                blue=blue,
            )

            timers.append(timer)

        return timers

    def update_state(self):
        """
        Updates the state of this controller
        """
        state = self._api.get_state(self._host, self._port)

        # update the controller values from the response
        self._device_name = state["device_name"]
        self._power_state = state["power_status"]
        self._function = state["mode"]
        self._function_speed = state["speed"]
        self._rgbww = (
            state["red"],
            state["green"],
            state["blue"],
            state["warm_white"],
            state["cold_white"]
        )
