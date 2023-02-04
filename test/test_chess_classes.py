import pytest
from chess_classes import Rook, Knight, Bishop, Queen, King, Pawn, Game, Colour


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
        [*[None] * 4, King(Colour.WHITE), *[None] * 2, Rook(Colour.WHITE)],
        [*[None] * 2, Pawn(Colour.WHITE), *[None] * 2, Pawn(Colour.WHITE), None, Pawn(Colour.WHITE)],
        [*[None] * 2, Knight(Colour.WHITE), *[None] * 5],
        [None] * 8,
        [*[None] * 3, Queen(Colour.WHITE), Pawn(Colour.WHITE), Pawn(Colour.BLACK), *[None] * 2],
        [None] * 8,
        [*[None] * 3, Pawn(Colour.BLACK), *[None] * 3, Pawn(Colour.WHITE)],
        [Rook(Colour.BLACK), *[None] * 3, King(Colour.BLACK), None, Bishop(Colour.BLACK), None]
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
        assert default_game.turn == Colour.BLACK
        default_game.change_turn()
        assert default_game.turn == Colour.WHITE

    # tests on custom position one
    def test_pawn_movement(self, custom_position_one):
        assert custom_position_one.move('c2a6') is False, "An illegal move has happened"
        assert custom_position_one.move('c2c4') is False, "Pawns can't move through a piece"
        assert custom_position_one.move('f2f4') is True, "Error for a pawn moving two squares"
        assert custom_position_one.move('e5e7') is False, "Can't move 2 steps forward if had been moved"
        assert custom_position_one.move('f2g3') is False, "Can't move sideways if not capture"


class TestBoard:

    # tests on custom position one
    def test_short_castle(self, custom_position_one):
        assert custom_position_one.board.short_castle(Colour.WHITE) is True, "Short castle logic is wrong"
        assert custom_position_one.board.short_castle(Colour.BLACK) is False, "Short castle logic is wrong"

    def test_long_castle(self, custom_position_one):
        assert custom_position_one.board.long_castle(Colour.BLACK) is True, "Long castle logic is wrong"
        assert custom_position_one.board.long_castle(Colour.WHITE) is False, "Long castle logic is wrong"

    def test_update_pawn_promotion(self, custom_position_one, monkeypatch):
        # mimic human input to promote to a Queen. Promotion to other pieces is identical
        monkeypatch.setattr('builtins.input', lambda _: "Q")
        assert custom_position_one.board.update(start=(6, 7), end=(7, 7)) is True
        assert isinstance(custom_position_one.board.state[7][7], Queen) is True, "Promotion did not happen or " \
                                                                                 "promoted to a wrong piece"
        assert custom_position_one.board.state[6][7] is None

    def test_update_king_moved_into_check(self, custom_position_one):
        assert custom_position_one.board.update(start=(7, 4), end=(6, 5)) is False

    def test_is_there_a_move(self, custom_position_one):
        assert custom_position_one.board.is_there_a_move(Colour.WHITE) is True, "is_there_a_move error"
        assert custom_position_one.board.is_there_a_move(Colour.BLACK) is True, "is_there_a_move error"

    def test_check_if_check(self, custom_position_one):
        assert custom_position_one.board.check_if_check(Colour.BLACK) is False, "check_if_check evaluates a position incorrectly"
        custom_position_one.move('d5f7')
        assert custom_position_one.board.check_if_check(Colour.BLACK) is True, "check_if_check evaluates a position incorrectly"


class TestPawn:

    # tests on custom position one
    def test_en_passant(self, custom_position_one):
        assert custom_position_one.move('e5f6') is True, "En passant hasn't happened"
        assert custom_position_one.board.state[4][5] is None, "En passant piece wasn't captured"

    def test_get_available_moves(self, custom_position_one):
        pawn_on_f2 = custom_position_one.board.state[1][5]
        pawn_on_f2.get_available_moves((1, 5), custom_position_one.board.state)
        assert pawn_on_f2.available_moves == [[2, 5], [3, 5]], \
            "Available moves for a pawn are found incorrectly"

        pawn_on_e5 = custom_position_one.board.state[4][4]
        pawn_on_e5.get_available_moves((4, 4), custom_position_one.board.state)
        assert pawn_on_e5.available_moves == [[5, 4], [5, 5]], \
            "Available moves for a pawn are found incorrectly"


class TestKnight:

    # tests on custom position one
    def test_get_available_moves(self, custom_position_one):
        knight_on_c3 = custom_position_one.board.state[2][2]
        knight_on_c3.get_available_moves((2, 2), custom_position_one.board.state)
        print(knight_on_c3.available_moves)
        assert knight_on_c3.available_moves == [[0, 1], [0, 3], [1, 0], [1, 4], [3, 0], [3, 4], [4, 1]], \
            "Available moves for a knight are found incorrectly"


class TestKing:

    # tests on custom position one
    def test_get_available_moves(self, custom_position_one):
        king_on_e8 = custom_position_one.board.state[7][4]
        king_on_e8.get_available_moves((7, 4), custom_position_one.board.state)
        assert king_on_e8.available_moves == [[6, 4], [6, 5], [7, 3], [7, 5]], \
            "Available moves for a king are found incorrectly"


class TestRook:

    # tests on custom position one
    def test_get_available_moves(self, custom_position_one):
        rook_on_h1 = custom_position_one.board.state[0][7]
        rook_on_h1.get_available_moves((0, 7), custom_position_one.board.state)
        assert rook_on_h1.available_moves == [[0, 5], [0, 6]], \
            "Available moves for a rook are found incorrectly"

        rook_on_a8 = custom_position_one.board.state[7][0]
        rook_on_a8.get_available_moves((7, 0), custom_position_one.board.state)
        assert rook_on_a8.available_moves == [[0, 0], [1, 0], [2, 0], [3, 0], [4, 0], [5, 0],
                                              [6, 0], [7, 1], [7, 2], [7, 3]], \
            "Available moves for a rook are found incorrectly"


class TestBishop:

    # tests on custom position one
    def test_get_available_moves(self, custom_position_one):
        bishop_on_g8 = custom_position_one.board.state[7][6]
        bishop_on_g8.get_available_moves((7, 6), custom_position_one.board.state)
        assert bishop_on_g8.available_moves == [[4, 3], [5, 4], [6, 5], [6, 7]], \
            "Available moves for a rook are found incorrectly"
