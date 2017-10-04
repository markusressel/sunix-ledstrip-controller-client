from enum import Enum


def _calculate_checksum(params: dict) -> int:
    """
    Calculates the checksum for a request

    :param params: request data 
    :return: checksum
    """

    checksum = 0
    for param in params:
        if param == "checksum":
            continue

        checksum += params[param]
        checksum = checksum % 0x100

    # print("checksum: " + hex(checksum))

    return checksum


def _evaluate_checksum(data: dict) -> bool:
    """
    Checks if a checksum is corrent

    :param data: the data packet to check 
    :return: True if the checksum is correct, false otherwise
    """

    if not data or not data["checksum"]:
        return False

    expected = _calculate_checksum(data)
    return data["checksum"] == expected


class TransitionType(Enum):
    """
    The transition type between colors of a custom function
    """

    Gradual = 0x3A
    Jumping = 0x3B
    Strobe = 0x3C
