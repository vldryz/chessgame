"""This module provides classes for chess pieces."""
# ——————————————————————————————————————————— Imports ——————————————————————————————————————————— #
# Dependencies
from pieces.piece_base import Piece
from utils import Colour

# ———————————————————————————————————————————— Code ———————————————————————————————————————————— #


class Pawn(Piece):
    def __init__(self, colour: Colour):
        super().__init__(colour, '♟' if colour == Colour.WHITE else '♙')

        # Pawn-specific attributes
        self.en_passant: bool = False

    def available_moves(self) -> list[tuple[int, int]]:
        ...


class King(Piece):
    def __init__(self, colour: Colour):
        super().__init__(colour, '♚' if colour == Colour.WHITE else '♔')

        # King-specific attributes
        self.checked: bool = False

    def available_moves(self) -> list[tuple[int, int]]:
        ...


class Knight(Piece):
    def __init__(self, colour: Colour):
        super().__init__(colour, '♞' if colour == Colour.WHITE else '♘')

    def available_moves(self) -> list[tuple[int, int]]:
        ...


class Bishop(Piece):
    def __init__(self, colour: Colour):
        super().__init__(colour, '♝' if colour == Colour.WHITE else '♗')

    def available_moves(self) -> list[tuple[int, int]]:
        ...


class Rook(Piece):
    def __init__(self, colour: Colour):
        super().__init__(colour, '♜' if colour == Colour.WHITE else '♖')

    def available_moves(self) -> list[tuple[int, int]]:
        ...


class Queen(Piece):
    def __init__(self, colour: Colour):
        super().__init__(colour, '♛' if colour == Colour.WHITE else '♕')

    def available_moves(self) -> list[tuple[int, int]]:
        ...
