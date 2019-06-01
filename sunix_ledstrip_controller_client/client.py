"""
Example usage of the ApiClient can be found in the example.py file
"""
import datetime
import logging
import queue
import socket
import threading
from queue import Queue

from sunix_ledstrip_controller_client.packets.responses import (Response, StatusResponse, SetTimeResponse,
                                                                GetTimeResponse, GetTimerResponse, SetPowerResponse)
from .functions import FunctionId
from .packets import TransitionType

logging.basicConfig(level=logging.WARNING, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.DEBUG)


class ApiClient:
    """
    This class is the main interface for controlling devices
    """

    def __init__(self, host: str, port: int, message_callback: callable = None):
        """
        Creates a new client object
        """
        self._keep_connections = True
        self._host = host
        self._port = port
        self._socket = None
        self._incoming_message_thread = None
        self._message_callback = message_callback

        self._received_messages = Queue()
        self._lock = threading.Lock()
        self._expect_response_types = {}

    def connect(self, reconnect: bool = False):
        """
        Connects to the controller

        :param reconnect: if True a new socket is created even if there is already an existing one,
                          otherwise an existing socket is reused
        """
        connection_key = "{}:{}".format(self._host, self._port)
        if reconnect:
            self.disconnect()

        if self._socket is None:
            LOGGER.debug("{} Connecting ...".format(connection_key))
            self._socket = socket.socket()
            self._socket.settimeout(1)
            self._socket.setblocking(True)
            self._socket.connect((self._host, self._port))

        if self._incoming_message_thread is None:
            self._incoming_message_thread = threading.Thread(name='background',
                                                             target=self._process_incoming_message,
                                                             daemon=True)
            self._incoming_message_thread.start()

    def _process_incoming_message(self):
        while self._socket is not None:
            message = self._listen_for_incoming_message()
            if message is not None:
                LOGGER.debug("Received: {}".format(message))
                if self._message_callback is not None:
                    self._message_callback(message)

                with self._lock:
                    response_type = type(message)
                    if response_type in self._expect_response_types:
                        amount = self._expect_response_types[response_type]
                        if amount <= 1:
                            self._expect_response_types.pop(response_type, None)
                        else:
                            self._expect_response_types[response_type] -= 1
                        self._received_messages.put(message)

    def reconnect(self):
        """
        Reconnects to the controller
        """
        LOGGER.debug("{}:{} Reconnecting...".format(self._host, self._port))
        self.disconnect()
        self.connect()

    @staticmethod
    def _get_response_instance(first: int, second: int) -> Response:
        if first == 129 and second == 37:
            return StatusResponse()
        elif first == 15 and second == 16:
            return SetTimeResponse()
        elif first == 15 and second == 17:
            return GetTimeResponse()
        elif first == 15 and second == 34:
            return GetTimerResponse()
        elif first == 15 and second == 113:
            return SetPowerResponse()
        else:
            raise AssertionError("Unknown response packet: {} {}".format(first, second))

    def _listen_for_incoming_message(self, response_length: int = 1) -> Response or bytes:
        if response_length is not None and response_length > 0:
            # at first always receive 2 bytes to detect response packet type and it's real length
            length = 2
            chunks = []
            bytes_recd = 0
            response_instance = None
            while bytes_recd < length:
                chunk = self._socket.recv(min(length - bytes_recd, 2048))
                if chunk == b'':
                    if self._socket is not None:
                        self.reconnect()
                    else:
                        return None
                chunks.append(chunk)
                bytes_recd = bytes_recd + len(chunk)

                if length == 2:
                    response_instance = self._get_response_instance(chunk[0], chunk[1])
                    length = response_instance.sizeof()

            # combine received chunks
            combined_bytes = b''.join(chunks)
            response_instance.parse_data(combined_bytes)
            LOGGER.debug(str(combined_bytes))
            return response_instance
        if response_length == -1:
            return self._socket.recv(2048)

    def disconnect(self):
        """
        Disconnects from the controller
        """
        LOGGER.debug("{}:{} Disconnecting".format(self._host, self._port))
        if self._socket is not None:
            try:
                s = self._socket
                self._socket = None
                s.shutdown(socket.SHUT_RDWR)
                s.close()
            except Exception as e:
                LOGGER.warning(e)

        if self._incoming_message_thread is not None:
            try:
                self._incoming_message_thread.join()
            except Exception as e:
                LOGGER.warning(e)
                pass
            finally:
                self._incoming_message_thread = None

    def _expect_response(self, type: type):
        """
        Indicates to the message thread that a response of the given type is expected
        :param type: the response type
        """
        with self._lock:
            if type in self._expect_response_types:
                self._expect_response_types[type] += 1
            else:
                self._expect_response_types[type] = 1

    def _find_first_response(self, type):
        timeout = 1
        start = datetime.datetime.now()
        try:
            while (datetime.datetime.now() - start).seconds < timeout:
                response = self._received_messages.get(block=True, timeout=timeout)
                if isinstance(response, type):
                    return response
        except queue.Empty as e:
            raise ValueError(
                "Expected response of type {} was not received within {} seconds".format(type, timeout))

    def get_time(self) -> Response:
        """
        Receives the current time of the specified controller

        :return: the current time of the controller
        """
        LOGGER.debug("{}:{} Retrieving time".format(self._host, self._port))
        from .packets.requests import GetTimeRequest

        self._expect_response(GetTimeResponse)
        request = GetTimeRequest()
        data = request.get_data()
        self._send_data(data)
        return self._find_first_response(GetTimeResponse)

    def set_time(self, date_time: datetime) -> Response:
        """
        Sets the internal time of the controller

        :param date_time: the time to set
        """
        LOGGER.debug("{}:{} Updating time".format(self._host, self._port))
        from .packets.requests import SetTimeRequest

        self._expect_response(SetTimeResponse)
        request = SetTimeRequest()
        data = request.get_data(date_time)
        self._send_data(data)
        return self._find_first_response(SetTimeResponse)

    def get_state(self) -> Response:
        """
        Requests a state update
        """
        LOGGER.debug("{}:{} Requesting state update".format(self._host, self._port))
        from .packets.requests import StatusRequest

        self._expect_response(StatusResponse)
        request = StatusRequest()
        data = request.get_data()
        self._send_data(data)
        return self._find_first_response(StatusResponse)

    def turn_on(self) -> Response:
        """
        Turns on a controller
        """
        LOGGER.debug("{}:{} Turning on".format(self._host, self._port))
        from .packets.requests import SetPowerRequest

        self._expect_response(SetPowerResponse)
        request = SetPowerRequest()
        data = request.get_data(True)
        self._send_data(data)
        return self._find_first_response(SetPowerResponse)

    def turn_off(self) -> Response:
        """
        Turns on a controller
        """
        LOGGER.debug("{}:{} Turning off".format(self._host, self._port))
        from .packets.requests import SetPowerRequest

        self._expect_response(SetPowerResponse)
        request = SetPowerRequest()
        data = request.get_data(False)
        self._send_data(data)
        return self._find_first_response(SetPowerResponse)

    def set_rgbww(self, red: int, green: int, blue: int,
                  warm_white: int, cold_white: int) -> None:
        """
        Sets rgbww values for the specified controller.

        :param red: red intensity (0..255)
        :param green: green intensity (0..255)
        :param blue: blue intensity (0..255)
        :param warm_white: warm_white: warm white intensity (0..255)
        :param cold_white: cold white intensity (0..255)
        """
        LOGGER.debug("{}:{} Updating rgbww".format(self._host, self._port))
        self._validate_color((red, green, blue, warm_white, cold_white), 5)

        from .packets.requests import UpdateColorRequest

        request = UpdateColorRequest()
        data = request.get_rgbww_data(red, green, blue, warm_white, cold_white)
        self._send_data(data)

    def set_rgb(self, red: int, green: int, blue: int) -> None:
        """
        Sets rgbw values for the specified controller.

        :param red: red intensity (0..255)
        :param green: green intensity (0..255)
        :param blue: blue intensity (0..255)
        """
        LOGGER.debug("{}:{} Updating rgb".format(self._host, self._port))
        self._validate_color((red, green, blue), 3)

        from .packets.requests import UpdateColorRequest

        request = UpdateColorRequest()
        data = request.get_rgb_data(red, green, blue)
        self._send_data(data)

    def set_ww(self, warm_white: int, cold_white: int) -> None:
        """
        Sets warm white and cold white values for the specified controller.

        :param warm_white: warm white intensity (0..255)
        :param cold_white: cold white intensity (0..255)
        """
        LOGGER.debug("{}:{} Updating ww".format(self._host, self._port))
        self._validate_color((warm_white, cold_white), 2)

        from .packets.requests import UpdateColorRequest

        request = UpdateColorRequest()
        data = request.get_ww_data(warm_white, cold_white)
        self._send_data(data)

    @staticmethod
    def get_function_list() -> [FunctionId]:
        """
        :return: a list of all supported functions
        """
        return list(FunctionId)

    def set_function(self, function_id: FunctionId, speed: int) -> None:
        """
        Sets a function on the specified controller

        :param function_id: Function ID
        :param speed: function speed [0..255] 0 is slow, 255 is fast
        """
        LOGGER.debug("{}:{} Updating function".format(self._host, self._port))
        from .packets.requests import SetFunctionRequest

        request = SetFunctionRequest()
        data = request.get_data(function_id, speed)
        self._send_data(data)

    def set_custom_function(self, color_values: [(int, int, int, int)],
                            speed: int, transition_type: TransitionType = TransitionType.Gradual) -> None:

        """
        Sets a custom function on the specified controller

        :param color_values: a list of up to 16 color tuples of the form (red, green, blue) or (red, green, blue, unknown).
                             I couldn't figure out what the last parameter is used for so the rgb is a shortcut.
        :param transition_type: the transition type between colors
        :param speed: function speed [0..255] 0 is slow, 255 is fast
        """
        LOGGER.debug("{}:{} Updating custom function".format(self._host, self._port))
        for color in color_values:
            self._validate_color(color, len(color))

        from .packets.requests import SetCustomFunctionRequest

        request = SetCustomFunctionRequest()
        data = request.get_data(color_values, speed, transition_type)
        self._send_data(data)

    def get_timers(self) -> Response:
        """
        Receives the current timer configurations of the specified controller

        :return: the current timer configuration of the controller
        """
        LOGGER.debug("{}:{} Retrieving timers".format(self._host, self._port))
        from .packets.requests import GetTimerRequest

        self._expect_response(GetTimerResponse)
        request = GetTimerRequest()
        data = request.get_data()
        self._send_data(data)
        return self._find_first_response(GetTimerResponse)

    def _send_data(self, data: bytes) -> Response or None:
        """
        Sends a binary data request to the specified host and port.
        :param data: the binary(!) data to send
        """

        reconnect = not self._keep_connections
        for i in range(3):
            try:
                self.connect(reconnect)
                if self._keep_connections:
                    self._socket.send(data)
                else:
                    with self._socket as s:
                        s.send(data)
                return
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
