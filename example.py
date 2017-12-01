import time

from sunix_ledstrip_controller_client.client import LEDStripControllerClient
from sunix_ledstrip_controller_client.controller import Controller

api = LEDStripControllerClient()
devices = api.discover_controllers()

device = Controller(api, "192.168.2.23")


def color_test():
    device.turn_on()

    time.sleep(1)

    device.set_rgbww(0, 0, 0, 255, 255)

    time.sleep(1)

    device.set_rgbww(0, 0, 0, 255, 0)

    time.sleep(1)

    device.set_rgbww(255, 0, 0, 0, 0)

    time.sleep(1)

    device.set_rgbww(0, 0, 0, 255, 0)

    time.sleep(1)

    device.set_rgbww(0, 255, 0, 0, 0)

    time.sleep(1)

    device.set_rgbww(0, 0, 0, 255, 0)

    time.sleep(1)

    device.set_rgbww(0, 0, 255, 0, 0)

    time.sleep(1)

    device.set_rgbww(0, 0, 0, 255, 0)

    time.sleep(1)

    device.set_rgbww(0, 0, 0, 255, 255)

    time.sleep(1)

    device.turn_off()


# run a color test that cycles through all the base colors
color_test()

device.turn_on()

time.sleep(1)

device.set_rgbww(255, 0, 0, 255, 0)

time.sleep(1)

device.set_rgb(0, 0, 0)

time.sleep(1)

device.set_ww(0, 0)
