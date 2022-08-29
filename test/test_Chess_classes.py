import pytest
from Chess_classes import Board, Piece, Rook, Knight, Bishop, Queen, King, Pawn, Game


class TestGame:
    @pytest.fixture
    def my_game(self):
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
    def test_notation_to_coordinates(self, my_game, notation, expected):
        assert my_game.notation_to_coordinates(notation) == expected

    def test_increment_move(self, my_game):
        my_game.increment_move()
        assert my_game.move_number == 2

    def test_change_turn(self, my_game):
        my_game.change_turn()
        assert my_game.turn == 'B'
        my_game.change_turn()
        assert my_game.turn == 'W'
