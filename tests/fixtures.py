"""This module provides custom board fixtures for tests."""
# ——————————————————————————————————————————— Imports ——————————————————————————————————————————— #
# 3rd party libraries
import pytest

# Dependencies
from chess.board import Board, MoveOutcome
from chess.pieces import Pawn, Knight, Bishop, Rook, Queen, King
from chess.colour_and_aliases import Colour, Square

# —————————————————————————————————————————— Fixtures —————————————————————————————————————————— #


# [
#     [
#         Rook(Colour.WHITE),
#         Knight(Colour.WHITE),
#         Bishop(Colour.WHITE),
#         Queen(Colour.WHITE),
#         None,
#         Rook(Colour.WHITE),
#         None,
#         King(Colour.WHITE),
#     ],
#     [
#         Pawn(Colour.WHITE),
#         Pawn(Colour.WHITE),
#         Pawn(Colour.WHITE),
#         None,
#         Bishop(Colour.WHITE),
#         Queen(Colour.BLACK),
#         None,
#         Pawn(Colour.WHITE),
#     ],
#     [
#         None, None, None, None, None, None,
#         Pawn(Colour.BLACK),
#         None,
#     ],
#     [
#         None, None, None, None,
#         Pawn(Colour.WHITE),
#         None, Pawn(Colour.WHITE), None,
#     ],
#     [
#         None, None, None, None,
#         Pawn(Colour.BLACK), None, Knight(Colour.WHITE), None,
#     ],
#     [
#         Pawn(Colour.BLACK),
#         None, None, None, None,
#         Knight(Colour.BLACK), None, None,
#     ],
#     [
#         None, Pawn(Colour.BLACK), None, None, None,
#         King(Colour.BLACK),
#         Pawn(Colour.BLACK),
#         Pawn(Colour.BLACK),
#     ],
#     [
#         Rook(Colour.BLACK),
#         Knight(Colour.BLACK),
#         Rook(Colour.WHITE),
#         None, None,
#         Bishop(Colour.BLACK),
#         None,
#         Rook(Colour.BLACK),
#     ],
# ]


# mimic human input to promote to a Queen. Promotion to other pieces is identical
# monkeypatch.setattr('builtins.input', lambda _: "Q")

# @pytest.fixture
# def custom_position_one():
#     """
#     returns a Game instance of custom state
#     Used to test castles, en_passant, pawn promotion, movement, checks
#     """
#     game = Game()
#     game.move_number = 10
#
#     # custom position
#     game.board.state = [
#         [*[None] * 4, King(Colour.WHITE), *[None] * 2, Rook(Colour.WHITE)],
#         [*[None] * 2, Pawn(Colour.WHITE), *[None] * 2, Pawn(Colour.WHITE), None, Pawn(Colour.WHITE)],
#         [*[None] * 2, Knight(Colour.WHITE), *[None] * 5],
#         [None] * 8,
#         [*[None] * 3, Queen(Colour.WHITE), Pawn(Colour.WHITE), Pawn(Colour.BLACK), *[None] * 2],
#         [None] * 8,
#         [*[None] * 3, Pawn(Colour.BLACK), *[None] * 3, Pawn(Colour.WHITE)],
#         [Rook(Colour.BLACK), *[None] * 3, King(Colour.BLACK), None, Bishop(Colour.BLACK), None]
#     ]
#
#     # pawns were moved
#     game.board.state[6][7].has_moved = True
#     game.board.state[4][4].has_moved = True
#     game.board.state[4][5].has_moved = True
#
#     # on the last move Black played f7f5 with a pawn. It is available for en passant
#     game.board.state[4][5].en_passant = True
#     game.board.temp_pawn_pos = (4, 5)
#
#     return game

