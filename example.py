import time

from sunix_ledstrip_controller_client import LEDStripControllerClient
from sunix_ledstrip_controller_client.controller import Controller

controller = LEDStripControllerClient()
devices = controller.discover_devices()

device = Controller("192.168.2.23", None, None, None)

controller.turn_on(device)

time.sleep(1)

controller.turn_off(device)

time.sleep(1)

controller.turn_on(device)



#for device in devices:
#    controller.turn_on(devices[0])
