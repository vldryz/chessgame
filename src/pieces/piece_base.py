"""This module provides a base abstract class for chess pieces."""
# ——————————————————————————————————————————— Imports ——————————————————————————————————————————— #
# Standard libraries
from abc import ABC, abstractmethod

# Dependencies
from utils import Colour

# ———————————————————————————————————————————— Code ———————————————————————————————————————————— #


class Piece(ABC):
    """Base class for chess pieces."""
    def __init__(self, colour, icon):
        self.colour: Colour = colour
        self.icon: str = icon
        self.moved: bool = False

    def __str__(self):
        return self.icon

    @abstractmethod
    def available_moves(self) -> list[tuple[int, int]]:
        """Returns a list of available moves for the piece.

        Returns:
            list[tuple[int, int]]: A list of available moves for the piece.

        """
        raise NotImplementedError()

