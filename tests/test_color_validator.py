import unittest


class TestColorValidatorMethods(unittest.TestCase):
    def test_color_valid(self):
        """
        Checks if the color validator accepts a valid color
        """

        from sunix_ledstrip_controller_client import LEDStripControllerClient
        from random import randint

        # check a bunch of random values
        for i in range(1000):
            color = []

            # append random color channel values
            for c in range(randint(2, 4)):
                color.append(randint(0, 255))

            # convert to tuple
            color = tuple(color)
            # validate
            LEDStripControllerClient._validate_color(color, len(color))

    def test_color_invalid_size(self):
        """
        Checks if the color validator detects an unexpected color channel size
        """

        from sunix_ledstrip_controller_client import LEDStripControllerClient
        from random import randint

        # check a bunch of random values
        for i in range(10):
            color = []

            # append random color channel values
            for c in range(randint(2, 4)):
                color.append(randint(0, 255))

            # convert to tuple
            color = tuple(color)
            # validate
            with self.assertRaises(ValueError):
                LEDStripControllerClient._validate_color(color, len(color) + 1)

    def test_color_invalid_color_channel_value(self):
        """
        Checks if the color validator detects an invalid color channel value
        """

        from sunix_ledstrip_controller_client import LEDStripControllerClient
        from random import randint

        # check a bunch of random values
        for i in range(1000):
            invalid = False
            color = []
            # append random color channel values
            for c in range(randint(2, 4)):
                r = randint(-1, 1)
                if r is -1:
                    color.append(randint(-999, -1))
                    invalid = True
                if r is 0:
                    color.append(randint(0, 255))
                if r is 1:
                    color.append(randint(256, 999))
                    invalid = True

            # convert to tuple
            color = tuple(color)
            # only validate colors that we know have invalid channel values
            if invalid is True:
                with self.assertRaises(ValueError):
                    LEDStripControllerClient._validate_color(color, len(color))


if __name__ == '__main__':
    unittest.main()
