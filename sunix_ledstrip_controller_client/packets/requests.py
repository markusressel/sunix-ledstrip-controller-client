import datetime as datetime

from construct import Int8ub

from sunix_ledstrip_controller_client.functions import FunctionId
from sunix_ledstrip_controller_client.packets import TransitionType, Packet


class Request(Packet):
    """
    Base class for a request packet
    """

    _params = {}

    def _attach_checksum(self):
        """
        Attaches a checksum to the end of this packet
        """

        checksum = self._calculate_checksum(self._params)
        self._params["checksum"] = checksum


class GetTimeRequest(Request):
    """
    Request for the current time of the controller
    """

    def __init__(self):
        super().__init__(
            "packet_id" / Int8ub,

            "payload1" / Int8ub,
            "payload2" / Int8ub,

            # this value specifies if the gateway is accessible locally or remotely
            # the remote value is only used by the official app
            # 0x0F for local
            # 0xF0 for remote
            "remote_or_local" / Int8ub,

            "checksum" / Int8ub
        )

    def get_data(self) -> dict:
        """
        Generates a binary data packet containing the a request for the current time of the controller
        :return: binary data packet
        """
        self._params = dict(packet_id=0x11,
                            payload1=0x1A,
                            payload2=0x1B,
                            remote_or_local=0x0F,
                            checksum=0)

        self._attach_checksum()
        return self.build(self._params)


class SetTimeRequest(Request):
    """
    Request to set the current time of the controller
    """

    def __init__(self):
        super().__init__(
            "packet_id" / Int8ub,

            "payload1" / Int8ub,

            # the current year - 2000
            "year" / Int8ub,
            "month" / Int8ub,
            "day" / Int8ub,
            "hour" / Int8ub,
            "minute" / Int8ub,
            "second" / Int8ub,
            # from Monday (1) - Sunday (7)
            "weekday" / Int8ub,

            "payload2" / Int8ub,

            # this value specifies if the gateway is accessible locally or remotely
            # the remote value is only used by the official app
            # 0x0F for local
            # 0xF0 for remote
            "remote_or_local" / Int8ub,

            "checksum" / Int8ub
        )

    def get_data(self, dt: datetime) -> dict:
        """
        Generates a binary data packet containing the a request for the current time of the controller
        :return: binary data packet
        """
        self._params = dict(packet_id=0x10,
                            payload1=0x14,

                            year=dt.year - 2000,
                            month=dt.month,
                            day=dt.day,
                            hour=dt.hour,
                            minute=dt.minute,
                            second=dt.second,
                            weekday=dt.isoweekday(),

                            payload2=0x00,
                            remote_or_local=0x0F,
                            checksum=0)

        self._attach_checksum()
        return self.build(self._params)


class StatusRequest(Request):
    """
    Request for the current status of the controller
    """

    def __init__(self):
        super().__init__(
            "packet_id" / Int8ub,

            "payload1" / Int8ub,
            "payload2" / Int8ub,

            "checksum" / Int8ub
        )

    def get_data(self) -> dict:
        """
        Generates a binary data packet containing the a request for the current state of the controller
        :return: binary data packet
        """
        self._params = dict(packet_id=0x81,
                            payload1=0x8A,
                            payload2=0x8B,
                            checksum=0)

        self._attach_checksum()
        return self.build(self._params)


class SetPowerRequest(Request):
    """
    Request for changing the power state
    """

    def __init__(self):
        super().__init__(
            # this is the id of the action to perform
            "packet_id" / Int8ub,

            # this indicates the new power status (on/off)
            # 0x23 for on
            # 0x24 for off
            "power_status" / Int8ub,

            # this value specifies if the gateway is accessible locally or remotely
            # the remote value is only used by the official app
            # 0x0F for local
            # 0xF0 for remote
            "remote_or_local" / Int8ub,

            # this is a checksum of the data packet
            "checksum" / Int8ub
        )

    def get_data(self, on: bool) -> dict:
        """
        Generates a binary data packet containing the request to change the power state of the controller

        :param on: True if the controller should turn on, False for turning off
        :return: binary data packet
        """

        from sunix_ledstrip_controller_client.controller import Controller
        self._params = dict(packet_id=0x71,
                            power_status=Controller.POWER_STATE_ON if on else Controller.POWER_STATE_OFF,
                            remote_or_local=0x0F,
                            checksum=0)

        self._attach_checksum()
        return self.build(self._params)


class UpdateColorRequest(Request):
    """
    Request for changing the color state (incl. brightness)
    """

    def __init__(self):
        super().__init__(
            # this is the id of the action to perform
            "packet_id" / Int8ub,

            # these are the color values
            "red" / Int8ub,
            "green" / Int8ub,
            "blue" / Int8ub,
            "warm_white" / Int8ub,
            "cold_white" / Int8ub,

            # this value specifies if only rgb, only ww or both values will be used
            # 0xF0 will only update rgb
            # 0x0F will only update ww
            # 0xFF will update both
            # 0x00 will ignore both (has no use afaik)
            "rgbww_selection" / Int8ub,

            # this value specifies if the gateway is accessible locally or remotely
            # the remote value is only used by the official app
            # 0x0F for local
            # 0xF0 for remote
            "remote_or_local" / Int8ub,

            # this is a checksum of the data packet
            "checksum" / Int8ub
        )

    def get_rgbww_data(self, red: int, green: int, blue: int, warm_white: int, cold_white: int) -> dict:
        """
        Generates a binary data packet containing the request to change colors for all 5 channels
        
        :param red: red amount 
        :param green: green amount 
        :param blue: blue amount
        :param warm_white: warm white amount 
        :param cold_white: cold white amount
        :return: binary data packet
        """
        self._params = dict(packet_id=0x31,
                            red=red,
                            green=green,
                            blue=blue,
                            warm_white=warm_white,
                            cold_white=cold_white,
                            rgbww_selection=0xFF,
                            remote_or_local=0x0F,
                            checksum=0)

        self._attach_checksum()
        return self.build(self._params)

    def get_rgb_data(self, red: int, green: int, blue: int) -> dict:
        """
        Generates a binary data packet containing the request to change rgb colors

        :param red: red amount 
        :param green: green amount 
        :param blue: blue amount
        :return: binary data packet
        """

        self._params = dict(packet_id=0x31,
                            red=red,
                            green=green,
                            blue=blue,
                            warm_white=0,
                            cold_white=0,
                            rgbww_selection=0xF0,
                            remote_or_local=0x0F,
                            checksum=0)

        self._attach_checksum()
        return self.build(self._params)

    def get_ww_data(self, warm_white: int, cold_white: int) -> dict:
        """
        Generates a binary data packet containing the request to change ww colors

        :param warm_white: warm white amount 
        :param cold_white: cold white amount
        :return: binary data packet
        """

        self._params = dict(packet_id=0x31,
                            red=0,
                            green=0,
                            blue=0,
                            warm_white=warm_white,
                            cold_white=cold_white,
                            rgbww_selection=0x0F,
                            remote_or_local=0x0F,
                            checksum=0)

        self._attach_checksum()
        return self.build(self._params)


class SetFunctionRequest(Request):
    """
    Request for setting a function
    """

    def __init__(self):
        super().__init__(
            # this is the id of the action to perform
            "packet_id" / Int8ub,

            # the id of the function to set
            # have a look at functions.FunctionId for a complete list
            "function_id" / Int8ub,
            # the speed at which the function should change colors or strobe etc.
            # originally this value is inverted, meaning 0 is fastest and 255 is slowest
            "speed" / Int8ub,

            # this value specifies if the gateway is accessible locally or remotely
            # the remote value is only used by the official app
            # 0x0F for local
            # 0xF0 for remote
            "remote_or_local" / Int8ub,

            # this is a checksum of the data packet
            "checksum" / Int8ub
        )

    def get_data(self, function_id: FunctionId or str or int, speed: int) -> dict:
        """
        Generates a binary data packet containing the request to set a function
        
        :param function_id: ID of the function 
        :param speed: function speed [0..255] 0 is slow, 255 is fast
        :return: binary data packet
        """

        from sunix_ledstrip_controller_client import functions

        # try to accept str and int types
        if isinstance(function_id, str):
            function_id = FunctionId[function_id]
        if isinstance(function_id, int):
            function_id = FunctionId(function_id)

        if not functions.is_valid(function_id):
            raise ValueError("Invalid function id")

        if speed < 0 or speed > 255:
            raise ValueError("Invalid speed value! Expected 0-255, got: %d" % speed)

        self._params = dict(packet_id=0x61,
                            function_id=function_id.value,
                            speed=255 - speed,
                            remote_or_local=0x0F,
                            checksum=0)

        self._attach_checksum()
        return self.build(self._params)


class SetCustomFunctionRequest(Request):
    """
    Request for setting a function
    """

    def __init__(self):
        super().__init__(
            # this is the id of the action to perform
            "packet_id" / Int8ub,

            # these are the color values
            "red_1" / Int8ub,
            "green_1" / Int8ub,
            "blue_1" / Int8ub,
            "unknown_1" / Int8ub,

            "red_2" / Int8ub,
            "green_2" / Int8ub,
            "blue_2" / Int8ub,
            "unknown_2" / Int8ub,

            "red_3" / Int8ub,
            "green_3" / Int8ub,
            "blue_3" / Int8ub,
            "unknown_3" / Int8ub,

            "red_4" / Int8ub,
            "green_4" / Int8ub,
            "blue_4" / Int8ub,
            "unknown_4" / Int8ub,

            "red_5" / Int8ub,
            "green_5" / Int8ub,
            "blue_5" / Int8ub,
            "unknown_5" / Int8ub,

            "red_6" / Int8ub,
            "green_6" / Int8ub,
            "blue_6" / Int8ub,
            "unknown_6" / Int8ub,

            "red_7" / Int8ub,
            "green_7" / Int8ub,
            "blue_7" / Int8ub,
            "unknown_7" / Int8ub,

            "red_8" / Int8ub,
            "green_8" / Int8ub,
            "blue_8" / Int8ub,
            "unknown_8" / Int8ub,

            "red_9" / Int8ub,
            "green_9" / Int8ub,
            "blue_9" / Int8ub,
            "unknown_9" / Int8ub,

            "red_10" / Int8ub,
            "green_10" / Int8ub,
            "blue_10" / Int8ub,
            "unknown_10" / Int8ub,

            "red_11" / Int8ub,
            "green_11" / Int8ub,
            "blue_11" / Int8ub,
            "unknown_11" / Int8ub,

            "red_12" / Int8ub,
            "green_12" / Int8ub,
            "blue_12" / Int8ub,
            "unknown_12" / Int8ub,

            "red_13" / Int8ub,
            "green_13" / Int8ub,
            "blue_13" / Int8ub,
            "unknown_13" / Int8ub,

            "red_14" / Int8ub,
            "green_14" / Int8ub,
            "blue_14" / Int8ub,
            "unknown_14" / Int8ub,

            "red_15" / Int8ub,
            "green_15" / Int8ub,
            "blue_15" / Int8ub,
            "unknown_15" / Int8ub,

            "red_16" / Int8ub,
            "green_16" / Int8ub,
            "blue_16" / Int8ub,
            "unknown_16" / Int8ub,

            # the speed at which the function should change colors or strobe etc.
            # originally this value is inverted, meaning 0 is fastest and 255 is slowest
            "speed" / Int8ub,

            # the transition type between colors
            # have a look at the TransitionType enum for more info
            "transition_type" / Int8ub,

            # this value normaly specifies if only rgb, only ww or both values will be changed
            # this is not supported for custom functions though and can not be altered as it has no effect
            "rgbww_selection" / Int8ub,

            # this value specifies if the gateway is accessible locally or remotely
            # the remote value is only used by the official app
            # 0x0F for local
            # 0xF0 for remote
            "remote_or_local" / Int8ub,

            # this is a checksum of the data packet
            "checksum" / Int8ub
        )

    def get_data(self, colors: [(int, int, int, int)], speed: int, transition_type: TransitionType) -> dict:
        """
        Generates a binary data packet containing the request to set a function

        :param colors: a list of color tuples of the form (red, green, blue) or (red, green, blue, unknown).
                       I couldn't figure out what the last parameter is used for so the rgb is a shortcut.
        :param transition_type: the transition type between colors
        :param speed: function speed [0..255] 0 is slow, 255 is fast
        :return: binary data packet
        """

        # do a little input validation
        if len(colors) > 16:
            raise ValueError("Only up to 16 color states are supported! You provided %d :(" % len(colors))

        for color in colors:
            if len(color) is not 3 and len(color) is not 4:
                raise ValueError("Unexpected tuple size %d in color %s! Expected: 3 or 4" % (len(color), str(color)))

        if speed < 0 or speed > 255:
            raise ValueError("Invalid speed value! Expected 0-255, got: %d" % speed)

        processed_colors = []

        # set default values
        for i in range(16):
            processed_colors.append([0x01, 0x02, 0x03, 0x00])

        index_red = 0
        index_green = 1
        index_blue = 2
        index_brightness = 3

        # apply colors from arguments
        for color_idx, color in enumerate(colors):
            for channel_idx, value in enumerate(color):
                processed_colors[color_idx][channel_idx] = value

        self._params = dict(packet_id=0x51,

                            # config data
                            speed=255 - speed,
                            transition_type=transition_type.value,
                            rgbww_selection=0xFF,
                            remote_or_local=0x0F,

                            checksum=0)

        # append color data to dictionary
        for idx, color in enumerate(processed_colors):
            idx += 1
            self._params["red_%d" % idx] = color[index_red]
            self._params["green_%d" % idx] = color[index_green]
            self._params["blue_%d" % idx] = color[index_blue]
            self._params["unknown_%d" % idx] = color[index_brightness]

        self._attach_checksum()
        return self.build(self._params)


class GetTimerRequest(Request):
    """
    Request for getting a timer
    """

    def __init__(self):
        super().__init__(
            # this is the id of the action to perform
            "packet_id" / Int8ub,

            "arg1" / Int8ub,
            "arg2" / Int8ub,

            # this value specifies if the gateway is accessible locally or remotely
            # the remote value is only used by the official app
            # 0x0F for local
            # 0xF0 for remote
            "remote_or_local" / Int8ub,

            # this is a checksum of the data packet
            "checksum" / Int8ub
        )

    def get_data(self) -> dict:
        """
        Generates a binary data packet containing the request to get a timer

        :return: binary data packet
        """

        self._params = dict(packet_id=0x22,
                            arg1=0x2a,
                            arg2=0x2b,
                            remote_or_local=0x0F,
                            checksum=0)

        self._attach_checksum()
        return self.build(self._params)
