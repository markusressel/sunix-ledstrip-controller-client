class Controller:
    """
    Device class that represents a single controller
    """

    POWER_STATE_ON = 0x23
    POWER_STATE_OFF = 0x24

    DEFAULT_PORT = 5577

    def __init__(self, host: str, port: int = DEFAULT_PORT, hardware_id: str = None, model: str = None):
        """
        Creates a new controller device object
        
        :param host: host address of the controller device
        :param port: the port on which the controller device is listening
        """

        self._host = host
        if not port:
            self._port = self.DEFAULT_PORT
        else:
            self._port = port
        self._hardware_id = hardware_id
        self._model = model
        self._power_state = None
        self._rgbww = None

    def __str__(self):
        return ("Host: %s\n" % (self.get_host()) +
                "Port: %s\n" % (self.get_port()) +
                "Hardware ID: %s\n" % (self.get_hardware_id()) +
                "Model: %s" % (self.get_model()))

    def get_host(self) -> str or None:
        """
        :return: The IP/Host address of this device  
        """
        return self._host

    def get_port(self) -> int:
        """
        :return: The port of this device 
        """
        return self._port

    def get_hardware_id(self) -> str or None:
        """
        :return: The hardware ID of this device (f.ex. 'F0FE6B2333C6') 
        """
        return self._hardware_id

    def get_model(self) -> str or None:
        """
        :return: The model of this device 
        """
        return self._model

    def is_on(self) -> bool:
        """
        :return: True if the controller is turned on, false otherwise
        """
        return self._power_state is self.POWER_STATE_ON

    def get_rgbww(self) -> [int, int, int, int, int] or None:
        """
        :return: the RGB color values
        """
        return self._rgbww

    def get_brightness(self) -> int or None:
        """
        Note: this value is calculated in the library and not on the device
        :return: the brightness of the controller [0..255] or None if no value is set
        """
        if not self._rgbww:
            return None

        brightness = 0
        for color in self._rgbww:
            brightness += color

        return int(brightness / len(self._rgbww))
