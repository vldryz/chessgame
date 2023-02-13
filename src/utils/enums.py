"""Enum classes for the project."""
# ——————————————————————————————————————————— Imports ——————————————————————————————————————————— #
# Standard libraries
from enum import StrEnum, Enum

# ———————————————————————————————————————————— Code ———————————————————————————————————————————— #


class Colour(StrEnum):
    """Enum class for piece colours."""
    WHITE = "White"
    BLACK = "Black"


class Moves(Enum):
    """Enum class for moves."""
    DEFAULT = "default"
    PIECE_MOVE = "piece move"
    SHORT_CASTLE = "o-o"
    LONG_CASTLE = "o-o-o"


class Commands(Enum):
    """Enum class for commands."""
    YES = "yes"
    NO = "no"
    HELP = "help"
    EXIT = "exit"
    SAVE_MOVE_HISTORY = "save move history"
    RESET = "reset"
    RESIGN = "resign"
    DRAW = "draw"
    PRINT_BOARD = "print board"

    # Implement in the future
    LOAD = "load from move history"
