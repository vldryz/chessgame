"""This module provides tests for the Board class."""
# ——————————————————————————————————————————— Imports ——————————————————————————————————————————— #
# 3rd party libraries
import pytest

# Dependencies
from chess.board import Board, MoveOutcome
from chess.pieces import Pawn, Knight, Bishop, Rook, Queen, King
from chess.colour_and_aliases import Colour, Square

# ———————————————————————————————————————————— Tests ———————————————————————————————————————————— #
