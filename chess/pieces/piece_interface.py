"""This module provides an interface for chess pieces."""
# ——————————————————————————————————————————— Imports ——————————————————————————————————————————— #
# Standard libraries
from typing import Self
from abc import ABC, abstractmethod
from enum import StrEnum, property

# Dependencies
from chess.colour_and_aliases import Colour, Square

# ———————————————————————————————————————————— Code ———————————————————————————————————————————— #


class PieceIcon(StrEnum):
    """Enum for piece icons."""

    WHITE_PAWN = "♟"
    WHITE_KNIGHT = "♞"
    WHITE_BISHOP = "♝"
    WHITE_ROOK = "♜"
    WHITE_QUEEN = "♛"
    WHITE_KING = "♚"
    BLACK_PAWN = "♙"
    BLACK_KNIGHT = "♘"
    BLACK_BISHOP = "♗"
    BLACK_ROOK = "♖"
    BLACK_QUEEN = "♕"
    BLACK_KING = "♔"

    @classmethod
    def get_icon(cls, colour: Colour, piece_name: str) -> Self:
        """Get the icon of a piece.

        Args:
            colour (Colour): The colour of the piece.
            piece_name (str): The name of the piece.

        Returns:
            Self: The corresponding member of the class.

        """

        return cls[f"{colour.upper()}_{piece_name.upper()}"]


class Piece(ABC):
    """Interface class for chess pieces."""

    def __init__(self, colour):
        self.colour: Colour = colour
        self.icon: PieceIcon = PieceIcon.get_icon(colour, self.name)
        self.moved: bool = False

    def __str__(self) -> str:
        return self.icon

    @property
    def name(self) -> str:
        return self.__class__.__name__

    def __eq__(self, other: Self) -> bool:
        return (
            self.colour == other.colour
            and self.name == other.name
            and self.moved == other.moved
        )

    @abstractmethod
    def moves_to_consider(self, start: Square) -> list[Square]:
        """The method to get a list of moves to consider for a piece.

        Moves to consider are defined as moves to which a piece can
        technically move, given the starting position, regardless
        of the position of other pieces.

        Args:
            start (Square): The starting position of the piece.

        Returns:
            list[Square]: A list of moves to consider for the piece.

        """

        raise NotImplementedError()
