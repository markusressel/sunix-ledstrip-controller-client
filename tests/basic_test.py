import unittest

from sunix_ledstrip_controller_client import LEDStripControllerClient
from sunix_ledstrip_controller_client.controller import Controller


class TestStringMethods(unittest.TestCase):
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

        device = Controller(host)
        self.assertIsNotNone(device)

        self.assertEqual(device.get_host(), host)
        self.assertEqual(device.get_port(), Controller.DEFAULT_PORT)
        self.assertEqual(device.get_hardware_id(), None)
        self.assertEqual(device.get_model(), None)
        self.assertEqual(device.get_rgbww(), None)
        self.assertEqual(device.get_brightness(), None)

    def test_create_controller_custom(self):
        """
        Creates a controller using default values
        :return: 
        """
        host = "192.168.2.123"
        port = 12345
        hardware_id = "7D89D6789VVBGDJOFDJ"
        model = "The Best One Ever"

        device = Controller(host, port, hardware_id, model)
        self.assertIsNotNone(device)

        self.assertEqual(device.get_host(), host)
        self.assertEqual(device.get_port(), port)
        self.assertEqual(device.get_hardware_id(), hardware_id)
        self.assertEqual(device.get_model(), model)
        self.assertEqual(device.get_rgbww(), None)
        self.assertEqual(device.get_brightness(), None)


if __name__ == '__main__':
    unittest.main()
