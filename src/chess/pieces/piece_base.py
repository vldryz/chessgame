"""This module provides a base abstract class for chess pieces."""
# ——————————————————————————————————————————— Imports ——————————————————————————————————————————— #
# Standard libraries
from abc import ABC, abstractmethod

# Dependencies
from chess.board import Board
from chess.colours import Colour

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
    def legal_moves(self, start, board: Board) -> list[tuple[int, int]]:
        """The method to get a list of legal moves for a piece.

        Legal moves are defined as a subset of available moves
        that do not put the king in check.

        Args:
            start (tuple[int, int]): The starting position of the piece.
            board (Board): The board on which the piece is located.

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

        Args:
            start (tuple[int, int]): The starting position of the piece.
            board (Board): The board on which the piece is located.

        Returns:
            list[tuple[int, int]]: A list of available moves for the piece.

        """

        raise NotImplementedError()
