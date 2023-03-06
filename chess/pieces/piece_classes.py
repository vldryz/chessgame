"""This module provides classes for chess pieces."""
# ——————————————————————————————————————————— Imports ——————————————————————————————————————————— #
# Standard libraries
from itertools import product

# Dependencies
from chess.pieces.piece_base import Piece
from chess.colour import Colour

# ———————————————————————————————————————————— Code ———————————————————————————————————————————— #


class Pawn(Piece):
    def __init__(self, colour: Colour):
        super().__init__(colour, "♟" if colour == Colour.WHITE else "♙")

        # Pawn-specific attributes
        self.en_passant: bool = False

    def possible_moves(self, start: tuple[int, int]) -> list[tuple[int, int]]:

        diff = 1 if self.colour == Colour.WHITE else -1
        moves = [(start[0] + diff, start[1])]

        if start[1] != 0:
            moves.append((start[0] + diff, start[1] - 1))

        if start[1] != 7:
            moves.append((start[0] + diff, start[1] + 1))

        if not self.moved:
            moves.append((start[0] + 2 * diff, start[1]))

        return moves


class King(Piece):
    def __init__(self, colour: Colour):
        super().__init__(colour, "♚" if colour == Colour.WHITE else "♔")

        # King-specific attributes
        self.checked: bool = False

    def possible_moves(self, start: tuple[int, int]) -> list[tuple[int, int]]:
        moves = [
            (start[0] + rank, start[1] + file)
            for rank, file in product(range(-1, 2), range(-1, 2))
            if not rank == file == 0
        ]

        return list(filter(lambda move: 0 <= move[0] <= 7 and 0 <= move[1] <= 7, moves))


class Knight(Piece):
    def __init__(self, colour: Colour):
        super().__init__(colour, "♞" if colour == Colour.WHITE else "♘")

    def possible_moves(self, start: tuple[int, int]) -> list[tuple[int, int]]:
        moves = [
            (start[0] + rank, start[1] + file)
            for i, j in product((-1, 1), (-2, 2))
            for rank, file in {(i, j), (j, i)}
        ]

        return list(filter(lambda move: 0 <= move[0] <= 7 and 0 <= move[1] <= 7, moves))


class Bishop(Piece):
    def __init__(self, colour: Colour):
        super().__init__(colour, "♝" if colour == Colour.WHITE else "♗")

    def possible_moves(self, start: tuple[int, int]) -> list[tuple[int, int]]:
        moves = [
            (start[0] + rank, start[1] + file)
            for i, j in zip(range(1, 8), range(-1, -8, -1))
            for rank, file in {(i, j), (j, i), (-i, j), (i, -j)}
        ]

        return list(filter(lambda move: 0 <= move[0] <= 7 and 0 <= move[1] <= 7, moves))


class Rook(Piece):
    def __init__(self, colour: Colour):
        super().__init__(colour, "♜" if colour == Colour.WHITE else "♖")

    def possible_moves(self, start: tuple[int, int]) -> list[tuple[int, int]]:
        return [(start[0], file) for file in range(8) if file != start[1]] + [
            (rank, start[1]) for rank in range(8) if rank != start[0]
        ]


class Queen(Piece):
    def __init__(self, colour: Colour):
        super().__init__(colour, "♛" if colour == Colour.WHITE else "♕")

    def possible_moves(self, start: tuple[int, int]) -> list[tuple[int, int]]:
        moves = [
            (start[0] + rank, start[1] + file)
            for i, j in zip(range(1, 8), range(-1, -8, -1))
            for rank, file in {(i, j), (j, i), (-i, j), (i, -j)}
        ]

        moves = list(
            filter(lambda move: 0 <= move[0] <= 7 and 0 <= move[1] <= 7, moves)
        )

        moves.extend(
            [(start[0], file) for file in range(8) if file != start[1]]
            + [(rank, start[1]) for rank in range(8) if rank != start[0]]
        )

        return moves
