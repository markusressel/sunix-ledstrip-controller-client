import unittest


class TestTurnOnOffMethods(unittest.TestCase):
    def test_turn_on(self):
        """
        Checks basic turn on functionality
        """

        from sunix_ledstrip_controller_client.packets.requests import SetPowerRequest
        request = SetPowerRequest()
        data = request.get_data(True)

        self.assertIsNotNone(data)

    def test_turn_off(self):
        """
        Checks basic turn off functionality
        """

        from sunix_ledstrip_controller_client.packets.requests import SetPowerRequest
        request = SetPowerRequest()
        data = request.get_data(False)

        self.assertIsNotNone(data)


if __name__ == '__main__':
    unittest.main()
