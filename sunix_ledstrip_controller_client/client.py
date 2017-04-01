"""
Example usage of the LEDStripControllerClient can be found in the example.py file
"""
import socket
from socket import AF_INET, SOCK_DGRAM, SOL_SOCKET, SO_REUSEADDR, SO_BROADCAST

from sunix_ledstrip_controller_client.controller import Controller


class LEDStripControllerClient:
    """
    THis class is the main interface for controlling all devices
    """

    _discovery_port = 48899
    _discovery_message = b'HF-A11ASSISTHREAD'

    def __init__(self):
        """
        Creates a new client object
        """

    def discover_devices(self) -> [Controller]:
        """
        Sends a broadcast message to the local network.
        Listening devices will respond to this broadcast with their self description
        
        :return: a list of devices
        """
        discovered_devices = []

        cs = socket.socket(AF_INET, SOCK_DGRAM)
        cs.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        cs.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)

        cs.sendto(self._discovery_message, ('255.255.255.255', self._discovery_port))

        cs.setblocking(True)
        cs.settimeout(1)

        try:
            # TODO: allow multiple device detection

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

                device = Controller(ip, Controller.DEFAULT_PORT, hw_id, model)
                print(device)

                discovered_devices.append(device)
                return discovered_devices

        except socket.timeout:
            return discovered_devices

    def turn_on(self, device: Controller) -> None:
        """
        Turns on the given device
        :param: the device to turn on
        """

        self.send_packet(device.get_host(), device.get_port(), "on")

    def turn_off(self, device: Controller) -> None:
        """
        Turns on the given device
        :param: the device to turn on
        """

        self.send_packet(device.get_host(), device.get_port(), "off")

    def send_packet(self, host: str, port: int, action: str) -> None:

        from construct import Struct, Int8ub

        format = Struct(
            "packet_id" / Int8ub,
            "power_status" / Int8ub,
            "remote_or_local" / Int8ub,
            "checksum" / Int8ub
        )

        if action == "on":
            data = format.build(dict(packet_id=0x71, power_status=0x23, remote_or_local=0x0F, checksum=0xa3))
        else:
            data = format.build(dict(packet_id=0x71, power_status=0x24, remote_or_local=0x0F, checksum=0xa4))

        print(data)

        try:
            s = socket.socket()
            s.connect((host, port))

            s.send(data)

            s.setblocking(True)
            s.settimeout(1)

            data = s.recv(2048)

            print(data)

        except socket.timeout:
            pass
