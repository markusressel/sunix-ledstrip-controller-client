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

    if not data["checksum"]:
        return False

    expected = _calculate_checksum(data)
    return data["checksum"] == expected
