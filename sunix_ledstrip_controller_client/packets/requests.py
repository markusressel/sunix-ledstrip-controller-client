from construct import Struct, Int8ub


def calculate_checksum(params: dict) -> int:
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

    print("checksum: " + hex(checksum))

    return checksum


class SetPowerRequest(Struct):
    """
    Request for changing the power state
    """

    def __init__(self):
        super().__init__("packet_id" / Int8ub,
                         "power_status" / Int8ub,
                         "remote_or_local" / Int8ub,
                         "checksum" / Int8ub)

    def get_data(self, on: bool):
        params = dict(packet_id=0x71,
                      power_status=0x23 if on else 0x24,
                      remote_or_local=0x0F,
                      checksum=0xa3)

        checksum = calculate_checksum(params)
        params["checksum"] = checksum

        return self.build(params)


class UpdateColorRequest(Struct):
    """
    Request for changing the color state (incl. brightness)
    """

    def __init__(self):
        super().__init__("packet_id" / Int8ub,

                         "red" / Int8ub,
                         "green" / Int8ub,
                         "blue" / Int8ub,
                         "warm_white" / Int8ub,

                         "unused_payload" / Int8ub,

                         "set_warm_white" / Int8ub,

                         "remote_or_local" / Int8ub,

                         "checksum" / Int8ub)

    def get_rgb_data(self, red: int, green: int, blue: int):
        params = dict(packet_id=0x31,
                      red=red,
                      green=green,
                      blue=blue,
                      warm_white=0,
                      unused_payload=0,
                      set_warm_white=0xF0,
                      remote_or_local=0x0F,
                      checksum=0)

        checksum = calculate_checksum(params)
        params["checksum"] = checksum

        return self.build(params)

    def get_ww_data(self, warm_white: int):
        params = self.get_rgb_data(0, 0, 0)
        params["warm_white"] = warm_white
        params["set_warm_white"] = 0x0F

        checksum = calculate_checksum(params)
        params["checksum"] = checksum

        return self.build(params)
