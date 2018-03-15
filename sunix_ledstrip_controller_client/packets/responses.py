from construct import Int8ub

from sunix_ledstrip_controller_client.packets import Packet


class Response(Packet):
    """
    Base class for a response packet
    """
    _data = []

    def evaluate(self) -> bool:
        """
        :return: True if this response is valid, false otherwise
        """
        return self._evaluate_checksum(self.parse(self._data))

    def get_response(self) -> dict:
        """
        :return: the response in the expected format
        """
        if not self.evaluate():
            raise ValueError("invalid or missing checksum")

        return self.parse(self._data)


class StatusResponse(Response):
    """
    The response to the StatusRequest request
    """

    def __init__(self, data: bytearray):
        super().__init__(
            "packet_id" / Int8ub,

            "device_name" / Int8ub,
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

        self._data = data


class GetTimeResponse(Response):
    """
    The response to the GetTimeRequest request
    """

    def __init__(self, data: bytearray):
        super().__init__(
            "packet_id" / Int8ub,

            "unknown1" / Int8ub,
            "unknown2" / Int8ub,

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

        self._data = data


class GetTimerResponse(Response):
    """
    The response to the GetTimerRequest request
    """

    def __init__(self, data: bytearray):
        super().__init__(
            "packet_id" / Int8ub,

            "unknown_begin_1" / Int8ub,

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

        self._data = data
