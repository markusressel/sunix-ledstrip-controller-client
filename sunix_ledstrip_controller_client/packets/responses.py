from construct import Int8ub, Container

from sunix_ledstrip_controller_client.packets import Packet


class Response(Packet):
    """
    Base class for a response packet
    """
    _raw_data = []

    checksum = -1

    def evaluate(self, container: Container):
        """
        :return: True if this response is valid, false otherwise
        """
        self._evaluate_checksum(container)

    def parse_data(self, data: bytes) -> Container:
        """
        :return: the response in the expected format
        """
        self._raw_data = data
        parsed = self.parse(self._raw_data)

        self.evaluate(parsed)

        # save data on this object for easy access
        for k, v in parsed.items():
            setattr(self, k, v)

        return parsed


class StatusResponse(Response):
    """
    The response to the StatusRequest request
    """

    packet_id = 129
    device_name = 37

    power_status = -1
    mode = -1
    run_status = -1
    speed = -1

    red = -1
    green = -1
    blue = -1
    warm_white = -1
    unknown1 = -1
    cold_white = -1

    unknown2 = -1

    def __init__(self):
        super().__init__(
            "packet_id" / Int8ub,  # == 129

            "device_name" / Int8ub,  # == 37
            "power_status" / Int8ub,

            "mode" / Int8ub,
            "run_status" / Int8ub,
            "speed" / Int8ub,

            "red" / Int8ub,
            "green" / Int8ub,
            "blue" / Int8ub,
            "warm_white" / Int8ub,
            "unknown1" / Int8ub,
            "cold_white" / Int8ub,

            "unknown2" / Int8ub,

            "checksum" / Int8ub
        )


class SetTimeResponse(Response):
    """
    The response to the SetTimeRequest request
    """

    packet_id = 15
    device_name = 16

    def __init__(self):
        super().__init__(
            "packet_id" / Int8ub,  # == 15
            "device_name" / Int8ub,  # == 16
            "success" / Int8ub,
            "checksum" / Int8ub
        )


class SetPowerResponse(Response):
    """
    The empty response for a power request
    """

    packet_id = 15
    device_name = 113
    state = -1

    def __init__(self):
        super().__init__(
            "packet_id" / Int8ub,  # == 15
            "device_name" / Int8ub,  # == 113
            "state" / Int8ub,  # 35 == On, 36 == Off
            "checksum" / Int8ub
        )


class GetTimeResponse(Response):
    """
    The response to the GetTimeRequest request
    """

    packet_id = 15

    unknown1 = 17
    unknown2 = 20

    year = -1
    month = -1
    day = -1
    hour = -1
    minute = -1
    second = -1

    dayofweek = -1
    unknown3 = -1

    def __init__(self):
        super().__init__(
            "packet_id" / Int8ub,  # == 15

            "unknown1" / Int8ub,  # == 17
            "unknown2" / Int8ub,  # == 20

            # add 2000 to this value to get the correct year
            "year" / Int8ub,
            "month" / Int8ub,
            "day" / Int8ub,
            "hour" / Int8ub,
            "minute" / Int8ub,
            "second" / Int8ub,

            "dayofweek" / Int8ub,
            "unknown3" / Int8ub,

            "checksum" / Int8ub
        )


class GetTimerResponse(Response):
    """
    The response to the GetTimerRequest request
    """

    def __init__(self):
        super().__init__(
            "packet_id" / Int8ub,  # == 15

            "unknown_begin_1" / Int8ub,  # == 34

            "is_active_1" / Int8ub,

            # (0f=15??) add 2000 to this value to get the correct year
            "year_1" / Int8ub,
            "month_1" / Int8ub,
            "day_1" / Int8ub,
            "hour_1" / Int8ub,
            "minute_1" / Int8ub,
            "second_1" / Int8ub,

            # repeat mask
            # 0 = only once
            "dayofweek_1" / Int8ub,

            # 0x61 = color, 0x00, turn_on,
            "action_code_1" / Int8ub,

            # the actual color value
            "red_1" / Int8ub,
            "green_1" / Int8ub,
            "blue_1" / Int8ub,
            "warm_white_1" / Int8ub,
            "cold_white_1" / Int8ub,

            "unknown_end_1" / Int8ub,

            "is_active_2" / Int8ub,

            # (0f=15??) add 2000 to this value to get the correct year
            "year_2" / Int8ub,
            "month_2" / Int8ub,
            "day_2" / Int8ub,
            "hour_2" / Int8ub,
            "minute_2" / Int8ub,
            "second_2" / Int8ub,

            # repeat mask
            "dayofweek_2" / Int8ub,

            # 0x61 = color, 0x00, turn_on,
            "action_code_2" / Int8ub,

            # the actual color value
            "red_2" / Int8ub,
            "green_2" / Int8ub,
            "blue_2" / Int8ub,
            "warm_white_2" / Int8ub,
            "cold_white_2" / Int8ub,

            "unknown_end_2" / Int8ub,

            "is_active_3" / Int8ub,

            # (0f=15??) add 2000 to this value to get the correct year
            "year_3" / Int8ub,
            "month_3" / Int8ub,
            "day_3" / Int8ub,
            "hour_3" / Int8ub,
            "minute_3" / Int8ub,
            "second_3" / Int8ub,

            # repeat mask
            "dayofweek_3" / Int8ub,

            # 0x61 = color, 0x00, turn_on,
            "action_code_3" / Int8ub,

            # the actual color value
            "red_3" / Int8ub,
            "green_3" / Int8ub,
            "blue_3" / Int8ub,
            "warm_white_3" / Int8ub,
            "cold_white_3" / Int8ub,

            "unknown_end_3" / Int8ub,

            "is_active_4" / Int8ub,

            # (0f=15??) add 2000 to this value to get the correct year
            "year_4" / Int8ub,
            "month_4" / Int8ub,
            "day_4" / Int8ub,
            "hour_4" / Int8ub,
            "minute_4" / Int8ub,
            "second_4" / Int8ub,

            # repeat mask
            "dayofweek_4" / Int8ub,

            # 0x61 = color, 0x00, turn_on,
            "action_code_4" / Int8ub,

            # the actual color value
            "red_4" / Int8ub,
            "green_4" / Int8ub,
            "blue_4" / Int8ub,
            "warm_white_4" / Int8ub,
            "cold_white_4" / Int8ub,

            "unknown_end_4" / Int8ub,

            "is_active_5" / Int8ub,

            # (0f=15??) add 2000 to this value to get the correct year
            "year_5" / Int8ub,
            "month_5" / Int8ub,
            "day_5" / Int8ub,
            "hour_5" / Int8ub,
            "minute_5" / Int8ub,
            "second_5" / Int8ub,

            # repeat mask
            "dayofweek_5" / Int8ub,

            # 0x61 = color, 0x00, turn_on,
            "action_code_5" / Int8ub,

            # the actual color value
            "red_5" / Int8ub,
            "green_5" / Int8ub,
            "blue_5" / Int8ub,
            "warm_white_5" / Int8ub,
            "cold_white_5" / Int8ub,

            "unknown_end_5" / Int8ub,

            "is_active_6" / Int8ub,

            # (0f=15??) add 2000 to this value to get the correct year
            "year_6" / Int8ub,
            "month_6" / Int8ub,
            "day_6" / Int8ub,
            "hour_6" / Int8ub,
            "minute_6" / Int8ub,
            "second_6" / Int8ub,

            # repeat mask
            "dayofweek_6" / Int8ub,

            # 0x61 = color, 0x00, turn_on,
            "action_code_6" / Int8ub,

            # the actual color value
            "red_6" / Int8ub,
            "green_6" / Int8ub,
            "blue_6" / Int8ub,
            "warm_white_6" / Int8ub,
            "cold_white_6" / Int8ub,

            "unknown_end_6" / Int8ub,

            "unknown_end_7" / Int8ub,

            "checksum" / Int8ub
        )

        # data_as_int = []
        # data_as_hex = []
        # for byte in data:
        #     # int.from_bytes(byte, byteorder='big', signed=False)
        #     data_as_int.append(byte)
        #     data_as_hex.append(hex(byte))
