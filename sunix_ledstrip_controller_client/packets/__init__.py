from enum import Enum

from construct import Struct


class Packet(Struct):
    """
    Base class for a network packet
    """

    def _calculate_checksum(self, params: dict) -> int:
        """
        Calculates the checksum for a request

        :param params: request data
        :return: checksum
        """

        checksum = 0
        for param in params:
            if param == "checksum" or param == "_io":
                continue

            checksum += params[param]
            checksum = checksum % 0x100

        # print("checksum: " + hex(checksum))

        return checksum

    def _evaluate_checksum(self, data: dict) -> bool:
        """
        Checks if a checksum is correct

        :param data: the data packet to check
        :return: True if the checksum is correct, false otherwise
        """

        if not data or "checksum" not in data:
            return False

        expected = self._calculate_checksum(data)
        return data["checksum"] == expected


class TransitionType(Enum):
    """
    The transition type between colors of a custom function
    """

    Gradual = 0x3A
    Jumping = 0x3B
    Strobe = 0x3C
