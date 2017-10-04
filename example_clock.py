import datetime

from sunix_ledstrip_controller_client import LEDStripControllerClient
from sunix_ledstrip_controller_client.controller import Controller

api = LEDStripControllerClient()
# devices = api.discover_controllers()

device = Controller("192.168.2.23")

print(api.get_time(device))

dt = datetime.datetime.now()
api.set_time(device, dt)

print(api.get_time(device))
