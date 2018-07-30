import unittest


class TestPackets(unittest.TestCase):

    def test_parse_response_data_1(self):
        """
        Checks if response parsing works as expected
        """

        from sunix_ledstrip_controller_client.packets.responses import StatusResponse

        data = b'\x81%#a!\x05\xff\xff\xff\xff\x01\xff\xffK'
        valid = StatusResponse(data).evaluate()

        self.assertEqual(valid, True)

    def test_parse_response_data_2(self):
        """
        Checks if response parsing works as expected
        """

        from sunix_ledstrip_controller_client.packets.responses import StatusResponse

        data = b'\x81%#a!\x0f\x00\x00\x00\xff\x01\xff\x0fh'
        valid = StatusResponse(data).evaluate()

        self.assertEqual(valid, True)

    def test_parse_response_data_3(self):
        """
        Checks if response parsing works as expected
        """

        from sunix_ledstrip_controller_client.packets.responses import StatusResponse

        data = b'\x81%#a!\x0f\x00\x00\x00\x00\x01\x00\xffZ'
        valid = StatusResponse(data).evaluate()

        self.assertEqual(valid, True)


if __name__ == '__main__':
    unittest.main()
