from sunix_ledstrip_controller_client import ApiClient
from sunix_ledstrip_controller_client.controller import Controller

api = ApiClient("192.168.2.23", 5577)

# use the raw api methods
api.turn_on()
api.set_rgbww(255, 255, 255, 255, 255)

# or use a controller class for convenient method access
device = Controller("192.168.2.23")

device.turn_on()
device.set_rgbww(255, 255, 255, 255, 255)
