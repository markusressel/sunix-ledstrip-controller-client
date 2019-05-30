import logging
import socket
from socket import AF_INET, SOCK_DGRAM, SOL_SOCKET, SO_REUSEADDR, SO_BROADCAST

from .controller import Controller

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.DEBUG)

_discovery_port = 48899
_discovery_message = b'HF-A11ASSISTHREAD'


def discover_controllers() -> [Controller]:
    """
    Sends a broadcast message to the local network.
    Listening devices will respond to this broadcast with their self description

    :return: a list of devices
    """
    discovered_controllers = set()

    # use discovery multiple times as controllers sometimes just don't respond
    for i in range(3):
        discovered_controllers.update(_discover_controllers())

    return list(discovered_controllers)


def _discover_controllers() -> [Controller]:
    """
    Internally used discovery method
    :return: list of discovered devices
    """
    discovered_controllers = []
    with socket.socket(AF_INET, SOCK_DGRAM) as cs:
        cs.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        cs.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)

        # send a local broadcast via udp with a "magic packet"
        cs.sendto(_discovery_message, ('255.255.255.255', _discovery_port))

        cs.setblocking(True)
        cs.settimeout(1)
        received_messages = []
        try:
            while True:
                data, address = cs.recvfrom(1024)
                received_messages.append(data.decode())

        except socket.timeout:
            if len(received_messages) <= 0:
                return []

    for message in received_messages:
        try:
            controller = _parse_discovery_response(message)
            discovered_controllers.append(controller)
        except Exception as e:
            LOGGER.error("Error parsing discovery message '{}': {}".format(message, e))
            print("Error parsing discovery message: %s" % message)
            return None

    return discovered_controllers


def _parse_discovery_response(message: str) -> Controller or None:
    """
    Parses a discovery response message and creates a Controller instance from it
    :param message: the received message
    :return: Controller instance or None if the message is invalid
    """
    # parse received message
    data = str.split(message, ",")

    # check validity
    if len(data) == 3:
        # extract data
        ip = data[0]
        hw_id = data[1]
        model = data[2]

        # create a Controller object representation
        return Controller(ip, Controller.DEFAULT_PORT, hw_id, model)
