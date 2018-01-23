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

            "is_active_1" / Int8ub,

            # (0f=15??) add 2000 to this value to get the correct year
            "year_1" / Int8ub,
            "month_1" / Int8ub,
            "day_1" / Int8ub,
            "hour_1" / Int8ub,
            "minute_1" / Int8ub,
            "second_1" / Int8ub,

            # repeat mask
            "dayofweek_1" / Int8ub,

            # 0x61 = color, 0x00, turn_on,
            "action_code_1" / Int8ub,

            # the actual color value
            "red" / Int8ub,
            "green" / Int8ub,
            "blue" / Int8ub,
            "warm_white" / Int8ub,
            "cold_white" / Int8ub,

            "unknown3" / Int8ub,

            "checksum" / Int8ub
        )

        self._data = data
