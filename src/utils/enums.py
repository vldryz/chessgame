"""Enum classes for the project."""
# ——————————————————————————————————————————— Imports ——————————————————————————————————————————— #
# Standard libraries
from enum import Enum

# ———————————————————————————————————————————— Code ———————————————————————————————————————————— #


class Colour(str, Enum):
    """Enum class for piece colours."""
    WHITE = 'W'
    BLACK = 'B'
