# the next 3 lines are to fix the relative import ImportError
import sys
from pathlib import Path
sys.path[0] = str(Path(sys.path[0]).parent)

import pytest
from Chess_classes import Board, Piece, Rook, Knight, Bishop, Queen, King, Pawn, Game


@pytest.fixture
def default_game():
    """
    returns a Game instance
    """
    return Game()


@pytest.fixture
def custom_position_one():
    """
    returns a Game instance of custom state
    Used to test castles, en_passant, pawn promotion, movement, checks
    """
    game = Game()
    game.move_number = 10

    # custom position
    game.board.state = [
        [None, None, None, None, King('W'), None, None, Rook('W')],
        [None, None, Pawn('W'), None, None, Pawn('W'), None, Pawn('W')],
        [None, None, Knight('W'), None, None, None, None, None],
        [None] * 8,
        [None, None, None, Queen('W'), Pawn('W'), Pawn('B'), None, None],
        [None] * 8,
        [None, None, None, Pawn('B'), None, None, None, Pawn('W')],
        [Rook('B'), None, None, None, King('B'), None, Bishop('B'), None]
    ]

    # pawns were moved
    game.board.state[6][7].has_moved = True
    game.board.state[4][4].has_moved = True
    game.board.state[4][5].has_moved = True

    # on the last move Black played f7f5 with a pawn. It is available for en passant
    game.board.state[4][5].en_passant = True
    game.board.temp_pawn_pos = (4, 5)

    return game


class TestGame:

    # tests on default game
    @pytest.mark.parametrize("notation,expected", [
        ('e4', (3, 4)),
        ('h8', (7, 7)),
        ('b9', False),
        ('k3', False)
    ])
    def test_notation_to_coordinates(self, default_game, notation, expected):
        assert default_game.notation_to_coordinates(notation) == expected

    def test_increment_move(self, default_game):
        default_game.increment_move()
        assert default_game.move_number == 2

    def test_change_turn(self, default_game):
        default_game.change_turn()
        assert default_game.turn == 'B'
        default_game.change_turn()
        assert default_game.turn == 'W'


class TestBoard:

    # tests on custom position one
    def test_short_castle(self, custom_position_one):
        assert custom_position_one.board.short_castle('W') is True, "Short castle logic is wrong"
        assert custom_position_one.board.short_castle('B') is False, "Short castle logic is wrong"

    def test_long_castle(self, custom_position_one):
        assert custom_position_one.board.long_castle('B') is True, "Long castle logic is wrong"
        assert custom_position_one.board.long_castle('W') is False, "Long castle logic is wrong"

    def test_update_pawn_promotion(self, custom_position_one, monkeypatch):
        # mimic human input to promote to a Queen. Promotion to other pieces is identical
        monkeypatch.setattr('builtins.input', lambda _: "Q")
        assert custom_position_one.board.update(start=(6, 7), end=(7, 7)) is True
        assert isinstance(custom_position_one.board.state[7][7], Queen) is True, "Promotion did not happen or" \
                                                                                 "promoted to a wrong piece"
        assert custom_position_one.board.state[6][7] is None
        print(custom_position_one.board)






    # def test_en_passant(self, custom_position_one):
    #     assert custom_position_one.board.update(start=(4, 4), end=(5, 5)) is True, "En passant logic is wrong"
    #     print(custom_position_one.board)
    #     assert custom_position_one.board.state[4][5] is None, "Pawn wasn't captured after en passant"
    #     assert isinstance(custom_position_one.board.state[5][5], Pawn) is True, "En passant logic is wrong"
    #     print(custom_position_one.board)

