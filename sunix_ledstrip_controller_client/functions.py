from enum import Enum


class FunctionId(Enum):
    SEVEN_COLOR_CROSS_FADE = 0x25
    RED_GRADUAL_CHANGE = 0x26
    GREEN_GRADUAL_CHANGE = 0x27
    BLUE_GRADUAL_CHANGE = 0x28
    YELLOW_GRADUAL_CHANGE = 0x29
    CYAN_GRADUAL_CHANGE = 0x2A
    PURPLE_GRADUAL_CHANGE = 0x2B
    WHITE_GRADUAL_CHANGE = 0x2C
    RED_GREEN_CROSS_FADE = 0x2D
    RED_BLUE_CROSS_FADE = 0x2E
    GREEN_BLUE_CROSS_FADE = 0x2F
    SEVEN_COLOR_STROBE_FLASH = 0x30
    RED_STROBE_FLASH = 0x31
    GREEN_STROBE_FLASH = 0x32
    BLUE_STROBE_FLASH = 0x33
    YELLOW_STROBE_FLASH = 0x34
    CYAN_STROBE_FLASH = 0x35
    PURPLE_STROBE_FLASH = 0x36
    WHITE_STROBE_FLASH = 0x37
    SEVEN_COLOR_JUMPING_CHANGE = 0x38
    NO_FUNCTION = 0x61


def is_valid(function_id: FunctionId):
    """
    Checks if a function_id is valid
     
    :param function_id: the value to check 
    :return: True if valid, false otherwise
    """
    if not function_id:
        return False

    for fid in FunctionId:
        if fid.value == function_id.value:
            return True

    return False
