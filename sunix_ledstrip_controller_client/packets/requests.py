from construct import Struct, Int8ub

from sunix_ledstrip_controller_client.functions import FunctionId
from sunix_ledstrip_controller_client.packets import _calculate_checksum


class StatusRequest(Struct):
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
        params = dict(packet_id=0x81,
                      payload1=0x8A,
                      payload2=0x8B,
                      checksum=0)

        checksum = _calculate_checksum(params)
        params["checksum"] = checksum

        return self.build(params)


class SetPowerRequest(Struct):
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
        params = dict(packet_id=0x71,
                      power_status=Controller.POWER_STATE_ON if on else Controller.POWER_STATE_OFF,
                      remote_or_local=0x0F,
                      checksum=0)

        checksum = _calculate_checksum(params)
        params["checksum"] = checksum

        return self.build(params)


class UpdateColorRequest(Struct):
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
        params = dict(packet_id=0x31,
                      red=red,
                      green=green,
                      blue=blue,
                      warm_white=warm_white,
                      cold_white=cold_white,
                      rgbww_selection=0xFF,
                      remote_or_local=0x0F,
                      checksum=0)

        checksum = _calculate_checksum(params)
        params["checksum"] = checksum

        return self.build(params)

    def get_rgb_data(self, red: int, green: int, blue: int) -> dict:
        """
        Generates a binary data packet containing the request to change rgb colors

        :param red: red amount 
        :param green: green amount 
        :param blue: blue amount
        :return: binary data packet
        """

        params = dict(packet_id=0x31,
                      red=red,
                      green=green,
                      blue=blue,
                      warm_white=0,
                      cold_white=0,
                      rgbww_selection=0xF0,
                      remote_or_local=0x0F,
                      checksum=0)

        checksum = _calculate_checksum(params)
        params["checksum"] = checksum

        return self.build(params)

    def get_ww_data(self, warm_white: int, cold_white: int) -> dict:
        """
        Generates a binary data packet containing the request to change ww colors

        :param warm_white: warm white amount 
        :param cold_white: cold white amount
        :return: binary data packet
        """

        params = dict(packet_id=0x31,
                      red=0,
                      green=0,
                      blue=0,
                      warm_white=warm_white,
                      cold_white=cold_white,
                      rgbww_selection=0x0F,
                      remote_or_local=0x0F,
                      checksum=0)

        checksum = _calculate_checksum(params)
        params["checksum"] = checksum

        return self.build(params)


class SetFunctionRequest(Struct):
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

    def get_data(self, function_id: FunctionId, speed: int) -> dict:
        """
        Generates a binary data packet containing the request to set a function
        
        :param function_id: ID of the function 
        :param speed: function speed [0..255] 0 is slow, 255 is fast
        :return: binary data packet
        """

        from sunix_ledstrip_controller_client import functions
        if not functions.is_valid(function_id):
            raise ValueError("Invalid function id")

        if speed < 0 or speed > 255:
            raise ValueError("Invalid speed value")

        params = dict(packet_id=0x61,
                      function_id=function_id.value,
                      speed=255 - speed,
                      remote_or_local=0x0F,
                      checksum=0)

        checksum = _calculate_checksum(params)
        params["checksum"] = checksum

        return self.build(params)
