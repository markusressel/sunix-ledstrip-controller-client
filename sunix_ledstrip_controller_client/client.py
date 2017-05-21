"""
Example usage of the LEDStripControllerClient can be found in the example.py file
"""
import socket
from socket import AF_INET, SOCK_DGRAM, SOL_SOCKET, SO_REUSEADDR, SO_BROADCAST

from sunix_ledstrip_controller_client.controller import Controller
from sunix_ledstrip_controller_client.functions import FunctionId
from sunix_ledstrip_controller_client.packets.requests import (
    StatusRequest, SetPowerRequest, UpdateColorRequest, SetFunctionRequest)
from sunix_ledstrip_controller_client.packets.responses import (
    StatusResponse)


class LEDStripControllerClient:
    """
    This class is the main interface for controlling all devices
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

        try:
            # TODO: allow multiple controller detection

            data, address = cs.recvfrom(4096)
            # print("Received message: \"%s\"" % data)
            # print("Address: " + address[0])

            message = data.decode()

            # print(message)

            # parse received message
            data = str.split(message, ",")

            # check validity
            if len(data) == 3:
                # extract data
                ip = data[0]
                hw_id = data[1]
                model = data[2]

                # create a Controller object representation
                controller = Controller(ip, Controller.DEFAULT_PORT, hw_id, model)
                print(controller)

                discovered_controllers.append(controller)
                return discovered_controllers

        except socket.timeout:
            return discovered_controllers

    def update_state(self, controller: Controller) -> None:
        """
        Updates the state of the passed in controller
        
        :param controller: the controller to update 
        """

        request = StatusRequest()
        data = request.get_data()

        response_data = self._send_data(controller.get_host(), controller.get_port(), data, True)

        # parse and check validity of response data
        status_response = StatusResponse(response_data).get_response()

        # update the controller values from the response
        controller._power_state = status_response["power_status"]
        controller._rgbww = [
            status_response["red"],
            status_response["green"],
            status_response["blue"],
            status_response["warm_white"],
            status_response["cold_white"]
        ]

    def turn_on(self, controller: Controller) -> None:
        """
        Turns on a controller
        :param controller: the controller to turn on
        """

        request = SetPowerRequest()
        data = request.get_data(True)

        self._send_data(controller.get_host(), controller.get_port(), data)
        self.update_state(controller)

    def turn_off(self, controller: Controller) -> None:
        """
        Turns on a controller
        :param controller: the controller to turn on
        """

        request = SetPowerRequest()
        data = request.get_data(False)

        self._send_data(controller.get_host(), controller.get_port(), data)
        self.update_state(controller)

    def set_rgbww(self, controller: Controller, red: int, green: int, blue: int,
                  warm_white: int, cold_white: int) -> None:
        """
        Sets rgbww values for the specified controller.
        
        :param controller: the controller to set the specified values on 
        :param red: red intensity (0..255)
        :param green: green intensity (0..255)
        :param blue: blue intensity (0..255)
        :param warm_white: warm_white: warm white intensity (0..255)
        :param cold_white: cold white intensity (0..255)
        """

        self.validate_color([red, green, blue, warm_white, cold_white], 5)

        request = UpdateColorRequest()
        data = request.get_rgbww_data(red, green, blue, warm_white, cold_white)

        self._send_data(controller.get_host(), controller.get_port(), data)
        self.update_state(controller)

    def set_rgb(self, controller: Controller, red: int, green: int, blue: int) -> None:
        """
        Sets rgbw values for the specified controller.
        
        :param controller: the controller to set the specified values on 
        :param red: red intensity (0..255)
        :param green: green intensity (0..255)
        :param blue: blue intensity (0..255)
        """

        self.validate_color([red, green, blue], 3)

        request = UpdateColorRequest()
        data = request.get_rgb_data(red, green, blue)

        self._send_data(controller.get_host(), controller.get_port(), data)
        self.update_state(controller)

    def set_ww(self, controller: Controller, warm_white: int, cold_white: int) -> None:
        """
        Sets warm white value for the specified controller.

        :param controller: the controller to set the specified values on 
        :param warm_white: warm white intensity (0..255)
        :param cold_white: cold white intensity (0..255)
        """

        self.validate_color([warm_white, cold_white], 2)

        request = UpdateColorRequest()
        data = request.get_ww_data(warm_white, cold_white)

        self._send_data(controller.get_host(), controller.get_port(), data)
        self.update_state(controller)

    def set_color_loop(self, *args: list([int, int, int, int, int])) -> None:
        """
        Set a custom color loop.
        :param args: 
        :return: 
        """
        for color in args:
            self.validate_color(color, 5)

        print(args)

    @staticmethod
    def validate_color(color: [int], color_channels: int) -> None:
        """
        Validates an int array that is meant to represent a color.
        If the color is valid this method will not do anything.
        There is no return value to check, the method will raise an Exception if necessary.
        
        :param color: the color array to validate
        :param color_channels: the expected amount of color channels in this color 
        """
        if len(color) != color_channels:
            raise ValueError(
                "Invalid size of color array. Expected " + str(color_channels) + ", got: " + str(len(color)))

        for color_channel in color:
            if color_channel < 0 or color_channel > 255:
                raise ValueError("Invalid color range! Expected 0-255, got: " + str(color_channel))

    def get_function_list(self) -> [FunctionId]:
        """
        :return: a list of all supported functions 
        """
        return list(FunctionId)

    def set_function(self, controller: Controller, function_id: FunctionId, speed: int):
        """
        Sets a function on the specified controller
        
        :param controller: the controller to set the function on 
        :param function_id: Function ID
        :param speed: speed of function
        """
        request = SetFunctionRequest()
        data = request.get_data(function_id, speed)

        self._send_data(controller.get_host(), controller.get_port(), data)

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
