from sunix_ledstrip_controller_client import Controller
from sunix_ledstrip_controller_client import TransitionType

device = Controller("192.168.2.33")

# create a list of color-channel tuples
colors = [(255, 0, 0, 255),
          (0, 255, 0),
          (0, 0, 255)]

# the function can (as far as I know) only control the RGB values, the WW values remain untouched.
# you can use this to your advantage (dimmed ambient white light) or simply turn the WW channels off beforehand
device.set_ww(0, 0)

# then set your custom function like this
device.set_custom_function(colors, 250, TransitionType.Gradual)
