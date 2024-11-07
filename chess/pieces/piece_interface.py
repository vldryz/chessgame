"""This module provides a base abstract class for chess pieces."""

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Self

from chess.colour_and_aliases import Square

if TYPE_CHECKING:
    from chess.colour_and_aliases import Colour


class Piece(ABC):
    """Interface class for chess pieces."""

    def __init__(self, colour: Colour, icon: str):
        self.colour: Colour = colour
        self.icon: str = icon
        self.moved: bool = False

    def __str__(self) -> str:
        return self.icon

    @property
    def name(self) -> str:
        """Piece name."""
        return self.__class__.__name__

    def __eq__(self, other: Self) -> bool:
        return (
            self.colour == other.colour and self.name == other.name and self.moved == other.moved
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
        raise NotImplementedError
