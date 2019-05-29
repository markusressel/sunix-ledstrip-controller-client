import unittest
from unittest.mock import MagicMock

from sunix_ledstrip_controller_client import ApiClient
from sunix_ledstrip_controller_client.controller import Controller
from sunix_ledstrip_controller_client.packets.responses import StatusResponse


class TestBasicMethods(unittest.TestCase):
    def test_create_controller(self):
        """
        Creates a controller using default values
        :return: 
        """
        host = "192.168.2.53"

        response_bytes = b'\x81%#a!\x05\x00\x00\x00\xff\x01\xff\xffN'
        response = StatusResponse()
        response.parse_data(response_bytes)
        ApiClient.get_state = MagicMock(return_value=response)

        device = Controller(host)
        device.update_state()
        self.assertIsNotNone(device)

        self.assertEqual(device.get_host(), host)
        self.assertEqual(device.get_port(), Controller.DEFAULT_PORT)
        self.assertEqual(device.get_hardware_id(), None)
        self.assertEqual(device.get_model(), None)
        self.assertEqual(device.get_rgbww(), (0, 0, 0, 255, 255))
        self.assertEqual(device.get_brightness(), 102)

    def test_create_controller_custom(self):
        """
        Creates a controller using default values
        :return:
        """
        host = "192.168.2.123"
        port = 12345
        hardware_id = "7D89D6789VVBGDJOFDJ"
        model = "The Best One Ever"

        response_bytes = b'\x81%#a!\x05\x00\x00\x00\xff\x01\xff\xffN'
        response = StatusResponse()
        response.parse_data(response_bytes)
        ApiClient.get_state = MagicMock(return_value=response)

        device = Controller(host, port, hardware_id, model)
        device.update_state()
        self.assertIsNotNone(device)

        self.assertEqual(device.get_host(), host)
        self.assertEqual(device.get_port(), port)
        self.assertEqual(device.get_hardware_id(), hardware_id)
        self.assertEqual(device.get_model(), model)
        self.assertEqual(device.get_rgbww(), (0, 0, 0, 255, 255))
        self.assertEqual(device.get_brightness(), 102)


if __name__ == '__main__':
    unittest.main()
