from construct import Struct, Int8ub

from sunix_ledstrip_controller_client.packets import _evaluate_checksum


class StatusResponse(Struct):
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

    def evaluate(self) -> bool:
        """
        :return: True if this response is valid, false otherwise 
        """
        return _evaluate_checksum(self.parse(self._data))

    def get_response(self) -> dict:
        """
        :return: the response in the expected format
        """
        if not self.evaluate():
            raise ValueError("invalid or missing checksum")

        return self.parse(self._data)
