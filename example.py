from sunix_ledstrip_controller_client import LEDStripControllerClient
from sunix_ledstrip_controller_client.controller import Controller

api = LEDStripControllerClient()
# devices = api.discover_devices()

device = Controller("192.168.2.23")

api.turn_on(device)

# time.sleep(1)
#
# api.turn_off(device)
#
# time.sleep(1)
#
# api.turn_on(device)


# api.set_rgbw(device, 255, 0, 0)
#
# time.sleep(1)
#
# api.set_rgbw(device, 0, 255, 0)
#
# time.sleep(1)
#
# api.set_rgbw(device, 0, 0, 255)
#
# time.sleep(1)
#
# api.set_rgbw(device, 255, 255, 255)


# for device in devices:
#    controller.turn_on(devices[0])
