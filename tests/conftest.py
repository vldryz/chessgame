"""This module provides custom chess fixtures for tests."""
from itertools import product

import pytest

from chess import Chess
from chess.board import Board
from chess.pieces import Pawn, Knight, Bishop, Rook, Queen, King
from chess.colour_and_aliases import Colour


@pytest.fixture
def game_one() -> Chess:
    """Pytest fixture for a custom board state.

    ♖  .  .  .  ♔  .  ♗  .    8
    .  .  .  ♙  .  .  .  ♟    7
    .  .  .  .  .  .  .  .    6
    .  .  .  ♛  ♟  ♙  .  .    5
    .  .  .  .  .  .  .  .    4
    .  .  ♞  .  .  .  .  .    3
    .  .  ♟  .  .  ♟  .  ♟    2
    .  .  .  .  ♚  .  .  ♜    1

    a  b  c  d  e  f  g  h

    Used to test castles, en_passant, pawn promotion, movement, checks.

    Returns:
        Chess: a Chess instance of custom state.

    """

    board = Board()

    board.state = [
        [
            *[None] * 4,
            King(Colour.WHITE),
            *[None] * 2,
            Rook(Colour.WHITE)],
        [
            *[None] * 2,
            Pawn(Colour.WHITE),
            *[None] * 2,
            Pawn(Colour.WHITE),
            None,
            Pawn(Colour.WHITE),
        ],
        [
            *[None] * 2,
            Knight(Colour.WHITE),
            *[None] * 5,
        ],
        [None] * 8,
        [
            *[None] * 3,
            Queen(Colour.WHITE),
            Pawn(Colour.WHITE),
            Pawn(Colour.BLACK),
            *[None] * 2,
        ],
        [None] * 8,
        [
            *[None] * 3,
            Pawn(Colour.BLACK),
            *[None] * 3,
            Pawn(Colour.WHITE),
        ],
        [
            Rook(Colour.BLACK),
            *[None] * 3,
            King(Colour.BLACK),
            None,
            Bishop(Colour.BLACK),
            None,
        ],
    ]

    # everything in the middle has moved
    for rank, file in product([2, 3, 4, 5], range(8)):
        if board.state[rank][file] is not None:
            board.state[rank][file].moved = True

    # h7 pawn has also moved
    board.state[6][7].moved = True

    # on the last move Black played f7f5 with a pawn. It is available for en passant
    board.en_passant_pawn = board.state[4][5]

    # Load the board into a Chess instance
    chess = Chess()
    chess.board = board
    chess.move_number = 15

    return chess


@pytest.fixture
def game_two() -> Chess:
    """Pytest fixture for a custom board state.

    ♖  ♘  ♜  .  .  ♗  .  ♖    8
    .  ♙  .  .  .  ♔  ♙  ♙    7
    ♙  .  .  .  .  ♘  .  .    6
    .  .  .  .  ♙  .  ♞  .    5
    .  .  .  .  ♟  .  ♟  .    4
    .  .  .  .  .  .  ♙  .    3
    ♟  ♟  ♟  .  ♝  ♕  .  ♟    2
    ♜  ♞  ♝  ♛  .  ♜  .  ♚    1

    a  b  c  d  e  f  g  h

    Used to test movement, checks, and checkmate.

    Returns:
        Chess: a Chess instance of custom state.

    """

    board = Board()

    board.state = [
        [
            Rook(Colour.WHITE),
            Knight(Colour.WHITE),
            Bishop(Colour.WHITE),
            Queen(Colour.WHITE),
            None,
            Rook(Colour.WHITE),
            None,
            King(Colour.WHITE),
        ],
        [
            Pawn(Colour.WHITE),
            Pawn(Colour.WHITE),
            Pawn(Colour.WHITE),
            None,
            Bishop(Colour.WHITE),
            Queen(Colour.BLACK),
            None,
            Pawn(Colour.WHITE),
        ],
        [
            *[None] * 6,
            Pawn(Colour.BLACK),
            None,
        ],
        [
            *[None] * 4,
            Pawn(Colour.WHITE),
            None,
            Pawn(Colour.WHITE),
            None,
        ],
        [
            *[None] * 4,
            Pawn(Colour.BLACK),
            None,
            Knight(Colour.WHITE),
            None,
        ],
        [
            Pawn(Colour.BLACK),
            *[None] * 4,
            Knight(Colour.BLACK),
            *[None] * 2,
        ],
        [
            None,
            Pawn(Colour.BLACK),
            *[None] * 3,
            King(Colour.BLACK),
            Pawn(Colour.BLACK),
            Pawn(Colour.BLACK),
        ],
        [
            Rook(Colour.BLACK),
            Knight(Colour.BLACK),
            Rook(Colour.WHITE),
            *[None] * 2,
            Bishop(Colour.BLACK),
            None,
            Rook(Colour.BLACK),
        ],
    ]

    # everything in the middle has moved
    for rank, file in product([2, 3, 4, 5], range(8)):
        if board.state[rank][file] is not None:
            board.state[rank][file].moved = True

    # c8, f7, f1, h1, e2, f2 have also moved
    squares = [(7, 2), (6, 5), (0, 5), (0, 7), (1, 4), (1, 5)]
    for rank, file in squares:
        board.state[rank][file].moved = True

    # Load the board into a Chess instance
    chess = Chess()
    chess.board = board
    chess.move_number = 8

    # Black's turn; Black is under check
    chess.turn = Colour.BLACK

    return chess
