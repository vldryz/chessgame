"""Enum classes for the project."""
# ——————————————————————————————————————————— Imports ——————————————————————————————————————————— #
# Standard libraries
from enum import StrEnum

# ———————————————————————————————————————————— Code ———————————————————————————————————————————— #


class Colour(StrEnum):
    """Enum class for piece colours."""
    WHITE = "white"
    BLACK = "black"

    def __str__(self) -> str:
        return self.value.title()
