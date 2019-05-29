from datetime import datetime

from sunix_ledstrip_controller_client import TransitionType
from sunix_ledstrip_controller_client.controller import Controller


def main():
    device1 = Controller("192.168.2.33")
    device1.connect()

    device1.turn_off()

    time_1 = device1.get_time()

    device1.set_rgb(5, 5, 5)
    device1.set_rgb(5, 5, 5)
    device1.set_rgb(5, 5, 5)
    device1.set_rgb(5, 5, 5)
    device1.set_rgb(5, 5, 5)
    device1.set_rgb(5, 5, 5)

    device1.turn_off()
    device1.turn_on()
    device1.turn_on()

    dt = datetime.now()
    device1.set_time(dt)
    device1.update_state()
    time_1 = device1.get_time()
    device1.set_time(time_1)

    device1.set_rgb(5, 5, 5)

    device1.set_rgb(5, 5, 5)
    device1.turn_on()
    device1.turn_on()

    device1.set_rgb(5, 5, 5)
    device1.update_state()
    device1.set_rgb(0, 5, 5)
    device1.update_state()
    device1.set_rgb(5, 0, 5)
    device1.update_state()
    device1.set_rgb(5, 5, 0)

    colors = [(255, 0, 0, 255),
              (0, 255, 0),
              (0, 0, 255)]
    device1.set_ww(0, 0)
    device1.set_custom_function(colors, 250, TransitionType.Gradual)
    device1.set_custom_function(colors, 250, TransitionType.Gradual)
    device1.update_state()
    device1.set_custom_function(colors, 250, TransitionType.Gradual)
    device1.set_custom_function(colors, 250, TransitionType.Gradual)

    device1.update_state()
    device1.turn_off()
    device1.update_state()

    dt = datetime.now()
    device1.set_time(dt)
    device1.update_state()
    time_1 = device1.get_time()
    device1.set_time(time_1)

    timers = device1.get_timers()
    device1.disconnect()


if __name__ == "__main__":
    main()
