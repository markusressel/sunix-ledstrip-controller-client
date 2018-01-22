import datetime

from sunix_ledstrip_controller_client import Controller
from sunix_ledstrip_controller_client import LEDStripControllerClient

api = LEDStripControllerClient()
# devices = api.discover_controllers()

device = Controller(api, "192.168.2.37")

# retrieve a list of all timers stored on the controller
timers = device.get_timers()
for timer in timers:
    print(timer)

# create a new timer
new_timer = Timer()

# create a datetime object
dt = datetime.datetime.now()
# and set this as the new current time of the controller
device.set_time(dt)

# print the result
print(device.get_time())
