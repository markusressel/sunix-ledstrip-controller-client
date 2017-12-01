import unittest
from unittest.mock import MagicMock

from sunix_ledstrip_controller_client import LEDStripControllerClient
from sunix_ledstrip_controller_client.controller import Controller


class TestBasicMethods(unittest.TestCase):
    def test_create_api(self):
        """
        Creates the api and object
        """

        api = LEDStripControllerClient()
        self.assertIsNotNone(api)

    def test_create_controller(self):
        """
        Creates a controller using default values
        :return: 
        """
        host = "192.168.2.53"

        api = LEDStripControllerClient()
        response_dict = {
            "device_name": "Test",
            "power_status": 0x24,
            "mode": "1",
            "speed": 255,
            "red": 255,
            "green": 255,
            "blue": 255,
            "warm_white": 255,
            "cold_white": 255,
        }
        api.get_state = MagicMock(return_value=response_dict)

        device = Controller(api, host)
        self.assertIsNotNone(device)

        self.assertEqual(device.get_host(), host)
        self.assertEqual(device.get_port(), Controller.DEFAULT_PORT)
        self.assertEqual(device.get_hardware_id(), None)
        self.assertEqual(device.get_model(), None)
        self.assertEqual(device.get_rgbww(), (255, 255, 255, 255, 255))
        self.assertEqual(device.get_brightness(), 255)

    def test_create_controller_custom(self):
        """
        Creates a controller using default values
        :return: 
        """
        host = "192.168.2.123"
        port = 12345
        hardware_id = "7D89D6789VVBGDJOFDJ"
        model = "The Best One Ever"

        api = LEDStripControllerClient()
        response_dict = {
            "device_name": "Test",
            "power_status": 0x24,
            "mode": "1",
            "speed": 255,
            "red": 255,
            "green": 255,
            "blue": 255,
            "warm_white": 255,
            "cold_white": 255,
        }
        api.get_state = MagicMock(return_value=response_dict)

        device = Controller(api, host, port, hardware_id, model)
        self.assertIsNotNone(device)

        self.assertEqual(device.get_host(), host)
        self.assertEqual(device.get_port(), port)
        self.assertEqual(device.get_hardware_id(), hardware_id)
        self.assertEqual(device.get_model(), model)
        self.assertEqual(device.get_rgbww(), (255, 255, 255, 255, 255))
        self.assertEqual(device.get_brightness(), 255)


if __name__ == '__main__':
    unittest.main()
