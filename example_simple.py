from sunix_ledstrip_controller_client import LEDStripControllerClient
from sunix_ledstrip_controller_client.controller import Controller
from sunix_ledstrip_controller_client.functions import FunctionId

api = LEDStripControllerClient()
# devices = api.discover_controllers()

device = Controller("192.168.2.23")

api.set_function(device, FunctionId.RED_GRADUAL_CHANGE, 240)

# api.turn_on(device)
#
# api.set_rgbww(device, 255, 255, 255, 255, 255)
#
# api.update_state(device)
#
