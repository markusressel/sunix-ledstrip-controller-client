from sunix_ledstrip_controller_client import LEDStripControllerClient
from sunix_ledstrip_controller_client.controller import Controller

api = LEDStripControllerClient()
devices = api.discover_controllers()

device = Controller("192.168.2.23")

api.turn_on(device)

api.set_rgbww(device, 255, 255, 255, 255, 255)

api.update_state(device)
