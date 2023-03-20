"""This module provides tests for chess pieces."""
# ——————————————————————————————————————————— Imports ——————————————————————————————————————————— #
# 3rd party libraries
import pytest

# Dependencies
from chess.pieces import Pawn, Knight, Bishop, Rook, Queen, King
from chess.colour_and_aliases import Colour, Square

# ———————————————————————————————————————————— Tests ———————————————————————————————————————————— #


class TestPawn:
    @pytest.mark.parametrize(
        "start, expected",
        [
            ((0, 0), [(1, 0), (1, 1), (2, 0)]),
            ((1, 1), [(2, 1), (2, 0), (2, 2), (3, 1)]),
            ((0, 7), [(1, 7), (1, 6), (2, 7)]),
            ((4, 4), [(5, 4), (5, 3), (5, 5), (6, 4)])
        ],
    )
    def test_white_moves_to_consider(self, start: Square, expected: list[Square]):
        pawn = Pawn(Colour.WHITE)
        assert pawn.moves_to_consider(start) == expected

    @pytest.mark.parametrize(
        "start, expected",
        [
            ((0, 0), [(1, 0), (1, 1)]),
            ((1, 1), [(2, 1), (2, 0), (2, 2)]),
            ((0, 7), [(1, 7), (1, 6)]),
            ((4, 4), [(5, 4), (5, 3), (5, 5)])
        ],
    )
    def test_white_pawn_moved_moves_to_consider(self, start: Square, expected: list[Square]):
        pawn = Pawn(Colour.WHITE)
        pawn.moved = True
        assert pawn.moves_to_consider(start) == expected

    @pytest.mark.parametrize(
        "start, expected",
        [
            ((7, 7), [(6, 7), (6, 6), (5, 7)]),
            ((6, 0), [(5, 0), (5, 1), (4, 0)]),
            ((6, 6), [(5, 6), (5, 5), (5, 7), (4, 6)]),
            ((4, 4), [(3, 4), (3, 3), (3, 5), (2, 4)]),
        ],
    )
    def test_black_moves_to_consider(self, start: Square, expected: list[Square]):
        pawn = Pawn(Colour.BLACK)
        assert pawn.moves_to_consider(start) == expected

    @pytest.mark.parametrize(
        "start, expected",
        [
            ((7, 7), [(6, 7), (6, 6)]),
            ((6, 0), [(5, 0), (5, 1)]),
            ((6, 6), [(5, 6), (5, 5), (5, 7)]),
            ((4, 4), [(3, 4), (3, 3), (3, 5)]),
        ],
    )
    def test_black_pawn_moved_moves_to_consider(self, start: Square, expected: list[Square]):
        pawn = Pawn(Colour.BLACK)
        pawn.moved = True
        assert pawn.moves_to_consider(start) == expected


class TestKing:
    @pytest.mark.parametrize(
        "start, expected",
        [
            ((0, 0), [(0, 1), (1, 0), (1, 1)]),
            ((1, 1), [(0, 0), (0, 1), (0, 2), (1, 0), (1, 2), (2, 0), (2, 1), (2, 2)]),
            ((4, 4), [(3, 3), (3, 4), (3, 5), (4, 3), (4, 5), (5, 3), (5, 4), (5, 5)]),
            ((0, 7), [(0, 6), (1, 6), (1, 7)]),
            ((7, 0), [(6, 0), (6, 1), (7, 1)]),
        ],
    )
    def test_moves_to_consider(self, start: Square, expected: list[Square]):
        king = King(Colour.WHITE)
        assert king.moves_to_consider(start) == expected


class TestKnight:
    @pytest.mark.parametrize(
        "start, expected",
        [
            ((0, 0), [(1, 2), (2, 1)]),
            ((1, 1), [(3, 0), (0, 3), (2, 3), (3, 2)]),
            ((7, 0), [(6, 2), (5, 1)]),
            ((4, 4), [(2, 3), (3, 2), (6, 3), (3, 6), (2, 5), (5, 2), (5, 6), (6, 5)]),
            ((2, 5), [(0, 4), (1, 3), (4, 4), (1, 7), (0, 6), (3, 3), (3, 7), (4, 6)]),
        ],
    )
    def test_moves_to_consider(self, start: Square, expected: list[Square]):
        knight = Knight(Colour.WHITE)
        assert knight.moves_to_consider(start) == expected


class TestBishop:
    @pytest.mark.parametrize(
        "start, expected",
        [
            (
                (0, 0),
                [
                    (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7),
                ]
            ),
            (
                (7, 7),
                [
                    (6, 6), (5, 5), (4, 4), (3, 3), (2, 2), (1, 1), (0, 0),
                ]
            ),
            (
                (7, 0),
                [
                    (6, 1), (5, 2), (4, 3), (3, 4), (2, 5), (1, 6), (0, 7),
                ]
            ),
            (
                (0, 7),
                [
                    (1, 6), (2, 5), (3, 4), (4, 3), (5, 2), (6, 1), (7, 0),
                ]
            ),
            (
                (4, 4),
                [
                    (3, 5), (5, 5), (3, 3), (5, 3), (6, 2), (2, 6), (2, 2), (6, 6), (1, 7),
                    (1, 1), (7, 1), (7, 7), (0, 0),
                ]
            ),
            (
                (2, 5),
                [
                    (1, 6), (3, 6), (1, 4), (3, 4), (4, 3), (0, 7), (0, 3), (4, 7), (5, 2),
                    (6, 1), (7, 0),
                ]
            ),
        ],
    )
    def test_moves_to_consider(self, start: Square, expected: list[Square]):
        bishop = Bishop(Colour.WHITE)
        assert bishop.moves_to_consider(start) == expected


class TestRook:
    @pytest.mark.parametrize(
        "start, expected",
        [
            (
                (0, 0),
                [
                    (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7), (1, 0), (2, 0),
                    (3, 0), (4, 0), (5, 0), (6, 0), (7, 0),
                ]
            ),
            (
                (7, 7),
                [
                    (7, 0), (7, 1), (7, 2), (7, 3), (7, 4), (7, 5), (7, 6), (0, 7), (1, 7),
                    (2, 7), (3, 7), (4, 7), (5, 7), (6, 7),
                ]
            ),
            (
                (7, 0),
                [
                    (7, 1), (7, 2), (7, 3), (7, 4), (7, 5), (7, 6), (7, 7), (0, 0), (1, 0),
                    (2, 0), (3, 0), (4, 0), (5, 0), (6, 0),
                ]
            ),
            (
                (0, 7),
                [
                    (0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (1, 7), (2, 7),
                    (3, 7), (4, 7), (5, 7), (6, 7), (7, 7),
                ]
            ),
            (
                (4, 4),
                [
                    (4, 0), (4, 1), (4, 2), (4, 3), (4, 5), (4, 6), (4, 7), (0, 4), (1, 4),
                    (2, 4), (3, 4), (5, 4), (6, 4), (7, 4),
                ]
            ),
            (
                (2, 5),
                [
                    (2, 0), (2, 1), (2, 2), (2, 3), (2, 4), (2, 6), (2, 7), (0, 5), (1, 5),
                    (3, 5), (4, 5), (5, 5), (6, 5), (7, 5),
                ]
            ),

        ],
    )
    def test_moves_to_consider(self, start: Square, expected: list[Square]):
        rook = Rook(Colour.WHITE)
        assert rook.moves_to_consider(start) == expected


class TestQueen:
    @pytest.mark.parametrize(
        "start, expected",
        [
            (
                (0, 0),
                [
                    (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (0, 1), (0, 2),
                    (0, 3), (0, 4), (0, 5), (0, 6), (0, 7), (1, 0), (2, 0), (3, 0), (4, 0),
                    (5, 0), (6, 0), (7, 0),
                ]
            ),
            (
                (7, 7),
                [
                    (6, 6), (5, 5), (4, 4), (3, 3), (2, 2), (1, 1), (0, 0), (7, 0), (7, 1),
                    (7, 2), (7, 3), (7, 4), (7, 5), (7, 6), (0, 7), (1, 7), (2, 7), (3, 7),
                    (4, 7), (5, 7), (6, 7),
                ]
            ),
            (
                (7, 0),
                [
                    (6, 1), (5, 2), (4, 3), (3, 4), (2, 5), (1, 6), (0, 7), (7, 1), (7, 2),
                    (7, 3), (7, 4), (7, 5), (7, 6), (7, 7), (0, 0), (1, 0), (2, 0), (3, 0),
                    (4, 0), (5, 0), (6, 0),
                ]
            ),
            (
                (0, 7),
                [
                    (1, 6), (2, 5), (3, 4), (4, 3), (5, 2), (6, 1), (7, 0), (0, 0), (0, 1),
                    (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (1, 7), (2, 7), (3, 7), (4, 7),
                    (5, 7), (6, 7), (7, 7),
                ]
            ),
            (
                (4, 4),
                [
                    (3, 5), (5, 5), (3, 3), (5, 3), (6, 2), (2, 6), (2, 2), (6, 6), (1, 7),
                    (1, 1), (7, 1), (7, 7), (0, 0), (4, 0), (4, 1), (4, 2), (4, 3), (4, 5),
                    (4, 6), (4, 7), (0, 4), (1, 4), (2, 4), (3, 4), (5, 4), (6, 4), (7, 4),
                ]
            ),
            (
                (2, 5),
                [
                    (1, 6), (3, 6), (1, 4), (3, 4), (4, 3), (0, 7), (0, 3), (4, 7), (5, 2),
                    (6, 1), (7, 0), (2, 0), (2, 1), (2, 2), (2, 3), (2, 4), (2, 6), (2, 7),
                    (0, 5), (1, 5), (3, 5), (4, 5), (5, 5), (6, 5), (7, 5),
                ]
            ),
        ],
    )
    def test_moves_to_consider(self, start: Square, expected: list[Square]):
        queen = Queen(Colour.WHITE)
        assert queen.moves_to_consider(start) == expected
