from dataclasses import dataclass
from enum import Enum
from pynput.keyboard import Controller, Key


class State(Enum):
    NORMAL = 0
    ERROR = 1
    ALL_CAPS = 2
    NO_CAPS = 3
    ALLOW_PUNCTUATION = 4
    DEFINE_PYTHON_VAR = 5
    ASLEEP = 6
    CAP_FIRST_LETTER = 8


@dataclass
class OutputSpec:
    """Class for keeping track of an item in inventory."""
    include_debug: bool = True
    emulate_keyboard: bool = False
    keyboard: Controller = None
    include_websocket: bool = False


