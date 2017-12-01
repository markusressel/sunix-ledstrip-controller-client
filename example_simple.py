from sunix_ledstrip_controller_client import LEDStripControllerClient
from sunix_ledstrip_controller_client.controller import Controller

api = LEDStripControllerClient()

# use the raw api methods
api.turn_on("192.168.2.23", 5577)
api.set_rgbww("192.168.2.23", 5577, 255, 255, 255, 255, 255)

# or use a controller class for convenient method access
device = Controller(api, "192.168.2.23")

device.turn_on()
device.set_rgbww(255, 255, 255, 255, 255)
