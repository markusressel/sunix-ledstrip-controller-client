import unittest

from sunix_ledstrip_controller_client import FunctionId


class TestFunctionMethods(unittest.TestCase):
    def test_function_codes_unique(self):
        """
        Checks if function codes are unique for each enum value
        """

        # check if function codes are unique
        for fun in FunctionId:
            for fun2 in FunctionId:
                if fun2.name is fun.name:
                    continue

                self.assertNotEqual(fun2.value, fun.value)

    def test_function_data_ok(self):
        """
        Tests the creation of a basic function packet
        """

        from sunix_ledstrip_controller_client.packets.requests import SetFunctionRequest
        request = SetFunctionRequest()

        for fun_id in FunctionId:
            for speed in range(256):
                data = request.get_data(fun_id, speed)
                self.assertIsNotNone(data)
                data2 = request.get_data(fun_id.name, speed)
                self.assertIsNotNone(data2)
                self.assertEqual(data, data2)

    def test_function_data_invalid_speed(self):
        """
        Tests the creation of a basic function packet with an invalid speed value
        """

        from sunix_ledstrip_controller_client.packets.requests import SetFunctionRequest
        request = SetFunctionRequest()

        for fun_id in FunctionId:
            for speed in [-1, 256]:
                with self.assertRaises(ValueError):
                    request.get_data(fun_id, speed)

    def test_function_data_invalid_function_id(self):
        """
        Tests the creation of a basic function packet with an invalid speed value
        """

        from sunix_ledstrip_controller_client.packets.requests import SetFunctionRequest
        request = SetFunctionRequest()

        with self.assertRaises(KeyError):
            request.get_data("invalid", speed=5)

        with self.assertRaises(ValueError):
            request.get_data(0x777, speed=5)

    def test_custom_function_data_ok(self):
        """
        Tests the creation of a basic function packet
        """

        from sunix_ledstrip_controller_client.packets.requests import SetCustomFunctionRequest
        from random import randint

        request = SetCustomFunctionRequest()

        for i in range(100):
            # generate color values
            color_values = []
            for i in range(randint(1, 16)):
                if randint(3, 4) is 3:
                    color_tuple = (randint(0, 255), randint(0, 255), randint(0, 255))
                else:
                    color_tuple = (randint(0, 255), randint(0, 255), randint(0, 255), randint(0, 255))
                color_values.append(color_tuple)

            speed = randint(0, 255)

            from sunix_ledstrip_controller_client.packets import TransitionType
            for transition_type in TransitionType:
                data = request.get_data(color_values, speed, transition_type)
                self.assertIsNotNone(data)


if __name__ == '__main__':
    unittest.main()
