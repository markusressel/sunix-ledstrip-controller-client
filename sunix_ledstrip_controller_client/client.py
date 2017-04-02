"""
Example usage of the LEDStripControllerClient can be found in the example.py file
"""
import socket
from socket import AF_INET, SOCK_DGRAM, SOL_SOCKET, SO_REUSEADDR, SO_BROADCAST

from sunix_ledstrip_controller_client.controller import Controller
from sunix_ledstrip_controller_client.packets.requests import SetPowerRequest, UpdateColorRequest


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

            data = str.split(message, ",")

            if len(data) == 3:
                ip = data[0]
                hw_id = data[1]
                model = data[2]

                controller = Controller(ip, Controller.DEFAULT_PORT, hw_id, model)
                print(controller)

                discovered_controllers.append(controller)
                return discovered_controllers

        except socket.timeout:
            return discovered_controllers

    def turn_on(self, controller: Controller) -> None:
        """
        Turns on a controller
        :param: the controller to turn on
        """

        request = SetPowerRequest()
        data = request.get_data(True)

        self._send_data(controller.get_host(), controller.get_port(), data)

    def turn_off(self, controller: Controller) -> None:
        """
        Turns on a controller
        :param: the controller to turn on
        """

        request = SetPowerRequest()
        data = request.get_data(False)

        self._send_data(controller.get_host(), controller.get_port(), data)

    def set_rgbww(self, controller: Controller, red: int, green: int, blue: int, warm_white: int,
                  cold_white: int) -> None:
        """
        Sets rgbww values for the specified controller.
        
        :param controller: the controller to set the specified values on 
        :param red: red intensity (0..255)
        :param green: green intensity (0..255)
        :param blue: blue intensity (0..255)
        :param warm_white: warm_white: warm white intensity (0..255)
        :param cold_white: cold white intensity (0..255)
        """

        request = UpdateColorRequest()
        data = request.get_rgbww_data(red, green, blue, warm_white, cold_white)

        self._send_data(controller.get_host(), controller.get_port(), data)

    def set_rgb(self, controller: Controller, red: int, green: int, blue: int) -> None:
        """
        Sets rgbw values for the specified controller.
        
        :param controller: the controller to set the specified values on 
        :param red: red intensity (0..255)
        :param green: green intensity (0..255)
        :param blue: blue intensity (0..255)
        """

        request = UpdateColorRequest()
        data = request.get_rgb_data(red, green, blue)

        print(data)

        self._send_data(controller.get_host(), controller.get_port(), data)

    def set_ww(self, controller: Controller, warm_white: int, cold_white: int) -> None:
        """
        Sets warm white value for the specified controller.

        :param controller: the controller to set the specified values on 
        :param warm_white: warm white intensity (0..255)
        :param cold_white: cold white intensity (0..255)
        """

        request = UpdateColorRequest()
        data = request.get_ww_data(warm_white, cold_white)

        print(data)

        self._send_data(controller.get_host(), controller.get_port(), data)

    @staticmethod
    def _send_data(host: str, port: int, data) -> None:
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

            s.setblocking(True)
            s.settimeout(1)

            data = s.recv(2048)

            print(data)

        except socket.timeout:
            print("timeout")
