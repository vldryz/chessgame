"""Enum classes for the project."""
# ——————————————————————————————————————————— Imports ——————————————————————————————————————————— #
# Standard libraries
from enum import Enum

# ———————————————————————————————————————————— Code ———————————————————————————————————————————— #


class Colour(str, Enum):
    """Enum class for piece colours."""
    WHITE = "White"
    BLACK = "Black"


class InputType(Enum):
    COMMAND = "command"
    MOVE = "move"


class Commands(Enum):
    """Enum class for commands."""
    YES = "yes"
    NO = "no"
    HELP = "help"
    EXIT = "exit"
    SAVE_MOVE_HISTORY = "save move history"
    RESET = "reset"
    SURRENDER = "surrender"
    RESIGN = "resign"
    DRAW = "draw"
    PRINT_BOARD = "print board"

    # Implement in the future
    LOAD = "load from move history"

    @staticmethod
    def values() -> set[str]:
        return {command.value for command in Commands}
