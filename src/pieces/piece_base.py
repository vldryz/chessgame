"""This module provides a base abstract class for chess pieces."""
# ——————————————————————————————————————————— Imports ——————————————————————————————————————————— #
# Standard libraries
from abc import ABC, abstractmethod

# Dependencies
from board import Board
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
    def legal_moves(self) -> list[tuple[int, int]]:
        """The method to get a list of legal moves for a piece.

        Legal moves are defined as a subset of available moves
        that do not put the king in check.

        Returns:
            list[tuple[int, int]]: A list of legal moves for the piece.

        """

        raise NotImplementedError()

    @abstractmethod
    def _available_moves(self, start, board: Board) -> list[tuple[int, int]]:
        """The method to get a list of available moves for a piece.

        Available moves are defined as moves to which a piece can
        technically move, regardless of whether it will put the king in check.
        Or in other words, the moves that are not blocked by other pieces.

        Returns:
            list[tuple[int, int]]: A list of available moves for the piece.

        """

        raise NotImplementedError()
