import datetime

from sunix_ledstrip_controller_client import Controller
from sunix_ledstrip_controller_client import LEDStripControllerClient

api = LEDStripControllerClient()
# devices = api.discover_controllers()

device = Controller(api, "192.168.2.37")

# print the current time of the controller
print(device.get_time())

# create a datetime object
dt = datetime.datetime.now()
# and set this as the new current time of the controller
device.set_time(dt)

# print the result
print(device.get_time())
