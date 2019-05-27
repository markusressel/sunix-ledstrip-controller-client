"""
Example usage of the LEDStripControllerClient can be found in the example.py file
"""
import datetime
import socket
from socket import AF_INET, SOCK_DGRAM, SOL_SOCKET, SO_REUSEADDR, SO_BROADCAST

from .controller import Controller
from .functions import FunctionId
from .packets import TransitionType


class LEDStripControllerClient:
    """
    This class is the main interface for controlling devices
    """

    _discovery_port = 48899
    _discovery_message = b'HF-A11ASSISTHREAD'

    def __init__(self, keep_connections: bool = False):
        """
        Creates a new client object

        :param keep_connections: if set to True tries to reuse the underlying socket for each controller as long
                                  as possible, otherwise a new socket will be used for each request
        """
        self._keep_connections = keep_connections
        self._connections = {}

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
            while True:
                data, address = cs.recvfrom(4096)
                received_messages.append(data.decode())

        except socket.timeout:
            if len(received_messages) <= 0:
                return discovered_controllers

        for message in received_messages:
            try:
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
            except:
                print("Error parsing discovery message: %s" % message)

        return discovered_controllers

    def connect_socket(self, host: str, port: int, reconnect: bool = False) -> socket:
        """
        Connects to the given host
        :param host: target host address
        :param port: target port
        :param reconnect: if True a new socket is created even if there is already an existing one,
                          otherwise an existing socket is reused
        :return: connected socket
        """
        # TODO: NEEDS TESTING does the controller send updates even when changes from other clients occur?
        connection_key = "{}:{}".format(host, port)
        if reconnect:
            self.disconnect_socket(host, port)

        if connection_key not in self._connections:
            s = socket.socket()
            s.settimeout(1)
            s.setblocking(True)
            self._connections[connection_key] = s
            s.connect((host, port))
        else:
            s = self._connections.get(connection_key)

        return s

    def disconnect_socket(self, host: str, port: int):
        """
        Disconnects from the given host
        :param host: target host address
        :param port: target port
        """
        connection_key = "{}:{}".format(host, port)
        if connection_key in self._connections:
            s = self._connections[connection_key]
            try:
                s.shutdown(socket.SHUT_RDWR)
                s.close()
            except Exception as e:
                pass
            finally:
                self._connections.pop(connection_key, None)

    def get_time(self, host: str, port: int) -> datetime:
        """
        Receives the current time of the specified controller

        :param host: controller host address
        :param port: controller port
        :return: the current time of the controller
        """
        from .packets.requests import GetTimeRequest
        from .packets.responses import GetTimeResponse

        request = GetTimeRequest()
        response = GetTimeResponse()

        data = request.get_data()
        response_data = self._send_data(host, port, data, response.sizeof())
        return response.parse_data(response_data)

    def set_time(self, host: str, port: int, date_time: datetime) -> dict:
        """
        Sets the internal time of the controller

        :param host: controller host address
        :param port: controller port
        :param date_time: the time to set
        """
        from .packets.requests import SetTimeRequest
        from .packets.responses import SetTimeResponse

        request = SetTimeRequest()
        response = SetTimeResponse()
        data = request.get_data(date_time)

        response_data = self._send_data(host, port, data, response.sizeof())
        return response.parse_data(response_data)

    def get_state(self, host: str, port: int) -> dict:
        """
        Updates the state of the passed in controller

        :param host: controller host address
        :param port: controller port
        """
        from .packets.requests import StatusRequest
        from .packets.responses import StatusResponse

        request = StatusRequest()
        response = StatusResponse()

        data = request.get_data()
        response_data = self._send_data(host, port, data, response.sizeof())
        return response.parse_data(response_data)

    def turn_on(self, host: str, port: int) -> None:
        """
        Turns on a controller

        :param host: controller host address
        :param port: controller port
        """
        from .packets.requests import SetPowerRequest

        request = SetPowerRequest()
        data = request.get_data(True)

        self._send_data(host, port, data, request.sizeof())

    def turn_off(self, host: str, port: int) -> None:
        """
        Turns on a controller

        :param host: controller host address
        :param port: controller port
        """
        from .packets.requests import SetPowerRequest

        request = SetPowerRequest()
        data = request.get_data(False)

        self._send_data(host, port, data, request.sizeof())

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

        from .packets.requests import UpdateColorRequest

        request = UpdateColorRequest()
        data = request.get_rgbww_data(red, green, blue, warm_white, cold_white)

        self._send_data(host, port, data, 0)

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

        from .packets.requests import UpdateColorRequest

        request = UpdateColorRequest()
        data = request.get_rgb_data(red, green, blue)

        self._send_data(host, port, data, 0)

    def set_ww(self, host: str, port: int, warm_white: int, cold_white: int) -> None:
        """
        Sets warm white and cold white values for the specified controller.

        :param host: controller host address
        :param port: controller port
        :param warm_white: warm white intensity (0..255)
        :param cold_white: cold white intensity (0..255)
        """
        self._validate_color((warm_white, cold_white), 2)

        from .packets.requests import UpdateColorRequest

        request = UpdateColorRequest()
        data = request.get_ww_data(warm_white, cold_white)

        self._send_data(host, port, data, 0)

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
        from .packets.requests import SetFunctionRequest

        request = SetFunctionRequest()
        data = request.get_data(function_id, speed)

        self._send_data(host, port, data, 0)

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

        from .packets.requests import SetCustomFunctionRequest

        request = SetCustomFunctionRequest()
        data = request.get_data(color_values, speed, transition_type)

        self._send_data(host, port, data, 0)

    def get_timers(self, host: str, port: int) -> dict:
        """
        Receives the current timer configurations of the specified controller

        :param host: controller host address
        :param port: controller port
        :return: the current timer configuration of the controller
        """
        from .packets.requests import GetTimerRequest
        from .packets.responses import GetTimerResponse

        request = GetTimerRequest()
        response = GetTimerResponse()

        data = request.get_data()
        response_data = self._send_data(host, port, data, response.sizeof())
        return response.parse_data(response_data)

    def _send_data(self, host: str, port: int, data: bytes,
                   response_size: int = 0) -> bytearray or None:
        """
        Sends a binary data request to the specified host and port.
        
        :param host: destination host
        :param port: destination port
        :param data: the binary(!) data to send
        """

        def receive_response() -> bytes:
            if response_size is not None and response_size > 0:
                chunks = []
                bytes_recd = 0
                while bytes_recd < response_size:
                    chunk = s.recv(min(response_size - bytes_recd, 2048))
                    if chunk == b'':
                        raise RuntimeError("socket connection broken")
                    chunks.append(chunk)
                    bytes_recd = bytes_recd + len(chunk)
                return b''.join(chunks)

        reconnect = not self._keep_connections
        for i in range(3):
            try:
                if self._keep_connections:
                    s = self.connect_socket(host, port, reconnect)
                    s.send(data)
                    return receive_response()
                else:
                    with self.connect_socket(host, port, reconnect) as s:
                        s.send(data)
                        return receive_response()
            except socket.error as e:
                reconnect = True

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
