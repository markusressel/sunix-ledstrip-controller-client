from sunix_ledstrip_controller_client.controller import Controller

# use a controller class for convenient method access
device = Controller("192.168.2.33")

device.turn_on()
device.set_rgbww(255, 255, 255, 255, 255)
