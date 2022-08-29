import pytest
from Chess_classes import Board, Piece, Rook, Knight, Bishop, Queen, King, Pawn, Game


@pytest.fixture
def my_game():
    """
    returns a Game instance
    """
    return Game()


@pytest.mark.parametrize("notation,expected", [
    ('e4', (3, 4)),
    ('h8', (7, 7)),
    ('b9', False),
    ('k3', False)
])
def test_notation_to_coordinates(my_game, notation, expected):
    assert my_game.notation_to_coordinates(notation) == expected

