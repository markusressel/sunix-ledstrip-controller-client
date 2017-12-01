"""
Example usage of the LEDStripControllerClient can be found in the example.py file
"""
import datetime
import socket
from socket import AF_INET, SOCK_DGRAM, SOL_SOCKET, SO_REUSEADDR, SO_BROADCAST

from sunix_ledstrip_controller_client.packets.responses import (
    StatusResponse, GetTimeResponse)
from .controller import Controller
from .functions import FunctionId
from .packets import TransitionType
from .packets.requests import (
    StatusRequest, SetPowerRequest, UpdateColorRequest, SetFunctionRequest, SetCustomFunctionRequest, GetTimeRequest,
    SetTimeRequest)


class LEDStripControllerClient:
    """
    This class is the main interface for controlling devices
    """

    _discovery_port = 48899
    _discovery_message = b'HF-A11ASSISTHREAD'

    def __init__(self):
        """
        Creates a new client object
        """

    def discover_controllers(self) -> [Controller]:
        """
        Sends a broadcast message to the local network.
        Listening devices will respond to this broadcast with their self description
        
        :return: a list of devices
        """
        discovered_controllers = []

        cs = socket.socket(AF_INET, SOCK_DGRAM)
        cs.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        cs.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)

        # send a local broadcast via udp with a "magic packet"
        cs.sendto(self._discovery_message, ('255.255.255.255', self._discovery_port))

        cs.setblocking(True)
        cs.settimeout(1)
        received_messages = []
        try:
            # TODO: allow multiple controller detection
            while True:
                data, address = cs.recvfrom(4096)
                # print("Received message: \"%s\"" % data)
                # print("Address: " + address[0])

                received_messages.append(data.decode())

        except socket.timeout:
            if len(received_messages) <= 0:
                return discovered_controllers

        for message in received_messages:
            # parse received message
            data = str.split(message, ",")

            # check validity
            if len(data) == 3:
                # extract data
                ip = data[0]
                hw_id = data[1]
                model = data[2]

                # create a Controller object representation
                controller = Controller(self, ip, Controller.DEFAULT_PORT, hw_id, model)
                print(controller)

                discovered_controllers.append(controller)

        return discovered_controllers

    def get_time(self, host: str, port: int) -> datetime:
        """
        Receives the current time of the specified controller

        :param host: controller host address
        :param port: controller port
        :return: the current time of the controller
        """

        request = GetTimeRequest()
        data = request.get_data()

        response_data = self._send_data(host, port, data, True)

        # parse and check validity of response data
        status_response = GetTimeResponse(response_data).get_response()

        dt = datetime.datetime(
            status_response["year"] + 2000,
            status_response["month"],
            status_response["day"],
            status_response["hour"],
            status_response["minute"],
            status_response["second"]
        )
        return dt

    def set_time(self, host: str, port: int, date_time: datetime) -> None:
        """
        Sets the internal time of the controller

        :param host: controller host address
        :param port: controller port
        :param date_time: the time to set
        """

        request = SetTimeRequest()
        data = request.get_data(date_time)

        self._send_data(host, port, data)

    def get_state(self, host: str, port: int) -> dict:
        """
        Updates the state of the passed in controller
        
        :param host: controller host address
        :param port: controller port
        """

        request = StatusRequest()
        data = request.get_data()

        response_data = self._send_data(host, port, data, True)

        # parse and check validity of response data
        status_response = StatusResponse(response_data).get_response()

        return status_response

    def turn_on(self, host: str, port: int) -> None:
        """
        Turns on a controller

        :param host: controller host address
        :param port: controller port
        """

        request = SetPowerRequest()
        data = request.get_data(True)

        self._send_data(host, port, data)

    def turn_off(self, host: str, port: int) -> None:
        """
        Turns on a controller

        :param host: controller host address
        :param port: controller port
        """

        request = SetPowerRequest()
        data = request.get_data(False)

        self._send_data(host, port, data)

    def set_rgbww(self, host: str, port: int, red: int, green: int, blue: int,
                  warm_white: int, cold_white: int) -> None:
        """
        Sets rgbww values for the specified controller.
        
        :param host: controller host address
        :param port: controller port
        :param red: red intensity (0..255)
        :param green: green intensity (0..255)
        :param blue: blue intensity (0..255)
        :param warm_white: warm_white: warm white intensity (0..255)
        :param cold_white: cold white intensity (0..255)
        """

        self._validate_color((red, green, blue, warm_white, cold_white), 5)

        request = UpdateColorRequest()
        data = request.get_rgbww_data(red, green, blue, warm_white, cold_white)

        self._send_data(host, port, data)

    def set_rgb(self, host: str, port: int, red: int, green: int, blue: int) -> None:
        """
        Sets rgbw values for the specified controller.
        
        :param host: controller host address
        :param port: controller port
        :param red: red intensity (0..255)
        :param green: green intensity (0..255)
        :param blue: blue intensity (0..255)
        """

        self._validate_color((red, green, blue), 3)

        request = UpdateColorRequest()
        data = request.get_rgb_data(red, green, blue)

        self._send_data(host, port, data)

    def set_ww(self, host: str, port: int, warm_white: int, cold_white: int) -> None:
        """
        Sets warm white and cold white values for the specified controller.

        :param host: controller host address
        :param port: controller port
        :param warm_white: warm white intensity (0..255)
        :param cold_white: cold white intensity (0..255)
        """

        self._validate_color((warm_white, cold_white), 2)

        request = UpdateColorRequest()
        data = request.get_ww_data(warm_white, cold_white)

        self._send_data(host, port, data)

    def get_function_list(self) -> [FunctionId]:
        """
        :return: a list of all supported functions 
        """
        return list(FunctionId)

    def set_function(self, host: str, port: int, function_id: FunctionId, speed: int):
        """
        Sets a function on the specified controller
        
        :param host: controller host address
        :param port: controller port
        :param function_id: Function ID
        :param speed: function speed [0..255] 0 is slow, 255 is fast
        """
        request = SetFunctionRequest()
        data = request.get_data(function_id, speed)

        self._send_data(host, port, data)

    def set_custom_function(self, host: str, port: int, color_values: [(int, int, int, int)],
                            speed: int, transition_type: TransitionType = TransitionType.Gradual):

        """
        Sets a custom function on the specified controller

        :param host: controller host address
        :param port: controller port
        :param color_values: a list of up to 16 color tuples of the form (red, green, blue) or (red, green, blue, unknown).
                             I couldn't figure out what the last parameter is used for so the rgb is a shortcut.
        :param transition_type: the transition type between colors
        :param speed: function speed [0..255] 0 is slow, 255 is fast
        """

        for color in color_values:
            self._validate_color(color, len(color))

        request = SetCustomFunctionRequest()
        data = request.get_data(color_values, speed, transition_type)

        self._send_data(host, port, data)

    @staticmethod
    def _send_data(host: str, port: int, data, wait_for_response: bool = False) -> bytearray or None:
        """
        Sends a binary data request to the specified host and port.
        
        :param host: destination host
        :param port: destination port
        :param data: the binary(!) data to send
        """

        try:
            s = socket.socket()
            s.connect((host, port))

            s.send(data)

            if wait_for_response:
                s.setblocking(True)
                s.settimeout(1)

                data = s.recv(2048)

                return data
            else:
                return None

        except socket.timeout:
            print("timeout")

    @staticmethod
    def _validate_color(color: (int, int, int), color_channels: int) -> None:
        """
        Validates an int tuple that is meant to represent a color.
        If the color is valid this method will not do anything.
        There is no return value to check, the method will raise an Exception if necessary.

        :param color: the color tuple to validate
        :param color_channels: the expected amount of color channels in this color
        """
        if len(color) != color_channels:
            raise ValueError(
                "Invalid amount of colors in color tuple. Expected " + str(color_channels) + ", got: " + str(
                    len(color)))

        for color_channel in color:
            if color_channel < 0 or color_channel > 255:
                raise ValueError("Invalid color range! Expected 0-255, got: " + str(color_channel))
