from sunix_ledstrip_controller_client import LEDStripControllerClient, FunctionId, TransitionType
from sunix_ledstrip_controller_client.controller import Controller

api = LEDStripControllerClient(reuse_connections=True)

device = Controller(api, "192.168.2.33")

device.connect()

# device.update_state()
# device.update_state()
#
# device.turn_off()
#
# device.update_state()
#
# device.turn_on()
# device.set_function(FunctionId.BLUE_GRADUAL_CHANGE, 100)
time = device.get_time()

device.disconnect()

device.set_function(FunctionId.NO_FUNCTION, 2)

device.turn_on()
device.set_rgb(5, 5, 5)
device.set_rgb(0, 5, 5)
device.set_rgb(5, 0, 5)
device.set_rgb(5, 5, 0)

colors = [(255, 0, 0, 255),
          (0, 255, 0),
          (0, 0, 255)]
device.set_ww(0, 0)
device.set_custom_function(colors, 250, TransitionType.Gradual)
device.set_custom_function(colors, 250, TransitionType.Gradual)
device.set_custom_function(colors, 250, TransitionType.Gradual)
device.set_custom_function(colors, 250, TransitionType.Gradual)

device.update_state()
device.update_state()

device.turn_off()

device.update_state()
device.update_state()
