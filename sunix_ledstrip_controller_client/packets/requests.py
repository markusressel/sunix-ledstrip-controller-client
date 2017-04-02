from construct import Struct, Int8ub

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
        params = dict(packet_id=0x71,
                      power_status=0x23 if on else 0x24,
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
