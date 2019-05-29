from sunix_ledstrip_controller_client import Controller

device = Controller("192.168.2.33")

# retrieve a list of all timers stored on the controller
timers = device.get_timers()
for timer in timers:
    print(timer)

# create a new timer
# new_timer = Timer()
