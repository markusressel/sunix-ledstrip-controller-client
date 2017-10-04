from sunix_ledstrip_controller_client import LEDStripControllerClient
from sunix_ledstrip_controller_client.controller import Controller
from sunix_ledstrip_controller_client.packets import TransitionType

api = LEDStripControllerClient()
# devices = api.discover_controllers()

device = Controller("192.168.2.23")

colors = [(255, 0, 0, 255),
          (0, 255, 0),
          (0, 0, 255)]

api.set_ww(device, 0, 0)
api.set_custom_function(device, colors, 250, TransitionType.Gradual)
