"""This module provides tests for the Board class."""
# ——————————————————————————————————————————— Imports ——————————————————————————————————————————— #
# 3rd party libraries
import pytest
from pytest import MonkeyPatch, CaptureFixture

# Dependencies
from chess import Chess
from chess.board import Board, MoveOutcome, _PromotionOption, _PromotionPiece
from chess.colour_and_aliases import Colour, Square

# ———————————————————————————————————————————— Tests ———————————————————————————————————————————— #


class TestDefaultBoard:
    """This class provides tests for the default board state.
    That is, the board state at the start of a game."""

    @pytest.mark.parametrize(
        "raw_input, turn, expected",
        [
            # valid moves
            ("e2e4", Colour.WHITE, MoveOutcome.SUCCESS),
            ("e2e3", Colour.WHITE, MoveOutcome.SUCCESS),
            ("b1c3", Colour.WHITE, MoveOutcome.SUCCESS),
            ("a2a3", Colour.WHITE, MoveOutcome.SUCCESS),
            ("g1h3", Colour.WHITE, MoveOutcome.SUCCESS),
            ("e7e5", Colour.BLACK, MoveOutcome.SUCCESS),
            ("a7a6", Colour.BLACK, MoveOutcome.SUCCESS),
            ("g8f6", Colour.BLACK, MoveOutcome.SUCCESS),

            # invalid moves
            ("o-o", Colour.WHITE, MoveOutcome.FAILURE),
            ("o-o-o", Colour.WHITE, MoveOutcome.FAILURE),
            ("o-o", Colour.BLACK, MoveOutcome.FAILURE),
            ("o-o-o", Colour.BLACK, MoveOutcome.FAILURE),
            ("a1a4", Colour.WHITE, MoveOutcome.FAILURE),
            ("a1c3", Colour.WHITE, MoveOutcome.FAILURE),
            ("e2e4", Colour.BLACK, MoveOutcome.FAILURE),
            ("b3b5", Colour.WHITE, MoveOutcome.FAILURE),
            ("", Colour.BLACK, MoveOutcome.FAILURE),
            ("nonsense", Colour.WHITE, MoveOutcome.FAILURE),
        ],
    )
    def test_make_move(self, raw_input: str, turn: Colour, expected: MoveOutcome, capfd: CaptureFixture):
        board = Board()
        assert board.make_move(raw_input, turn) == expected
        capfd.readouterr()  # clear stdout

    def test_moving_a_piece_sets_moved_attribute(self):
        """Test that moving a piece sets the moved attribute."""
        board = Board()

        assert board.state[1][4].moved is False
        board._move_piece(((1, 4), (3, 4)), Colour.WHITE)
        assert board.state[3][4].moved is True

        assert board.state[7][6].moved is False
        board._move_piece(((7, 6), (5, 5)), Colour.BLACK)
        assert board.state[5][5].moved is True

    def test_pawn_two_square_movement_sets_en_passant(self):
        """Test that a pawn moving two squares sets the en passant attribute.
        And that a move after it is removed"""

        board = Board()

        board._move_piece(((1, 4), (3, 4)), Colour.WHITE)
        assert board.en_passant_pawn is board.state[3][4]

        board._move_piece(((6, 4), (5, 4)), Colour.BLACK)
        assert board.en_passant_pawn is None

    @pytest.mark.parametrize(
        "start, end, turn, expected",
        [
            # valid moves
            ((1, 4), (2, 4), Colour.WHITE, True),
            ((0, 1), (2, 2), Colour.WHITE, True),
            ((0, 6), (2, 5), Colour.WHITE, True),
            ((1, 0), (2, 0), Colour.WHITE, True),
            ((1, 7), (2, 7), Colour.WHITE, True),
            ((6, 0), (5, 0), Colour.BLACK, True),
            ((7, 1), (5, 2), Colour.BLACK, True),
            ((7, 6), (5, 5), Colour.BLACK, True),

            # invalid moves
            ((1, 4), (4, 4), Colour.WHITE, False),
            ((1, 4), (7, 7), Colour.WHITE, False),
            ((1, 4), (0, 4), Colour.WHITE, False),
            ((7, 1), (6, 3), Colour.BLACK, False),
            ((7, 6), (7, 4), Colour.BLACK, False),
            ((7, 6), (6, 3), Colour.BLACK, False),
        ],
    )
    def test_move_piece(self, start: Square, end: Square, turn: Colour, expected: bool, capfd: CaptureFixture):
        """Test piece movement. Test that the state of the boards updates correctly"""

        board = Board()
        assert board._move_piece((start, end), turn) is expected

        if expected:
            assert board.state[start[0]][start[1]] is None
            assert board.state[end[0]][end[1]] is not None

        else:
            assert Board().state == board.state

        capfd.readouterr()  # clear stdout

    @pytest.mark.parametrize(
        "start, end, expected",
        [
            # valid moves
            ((1, 4), (2, 4), True),
            ((0, 1), (2, 2), True),
            ((0, 6), (2, 5), True),
            ((7, 1), (5, 2), True),
            ((7, 6), (5, 5), True),
            ((1, 0), (3, 0), True),
            ((1, 0), (2, 0), True),

            # invalid moves
            ((1, 4), (4, 4), False),
            ((1, 4), (2, 3), False),
            ((1, 4), (7, 7), False),
            ((1, 4), (0, 4), False),
            ((1, 4), (1, 3), False),
            ((0, 1), (2, 3), False),
            ((0, 1), (7, 7), False),
            ((7, 1), (7, 4), False),
            ((7, 1), (6, 3), False),
            ((7, 6), (5, 4), False),
            ((7, 6), (2, 5), False),
            ((7, 6), (7, 4), False),
            ((7, 6), (6, 3), False),
            ((1, 0), (4, 0), False),
            ((1, 0), (2, 1), False),
            ((1, 0), (7, 7), False),
        ],
    )
    def test_legal_move(self, start: Square, end: Square, expected: bool):
        """Test legal moves on move 1."""

        board = Board()
        assert board._legal_move(start, end) is expected
        assert board.state == Board().state

    @pytest.mark.parametrize(
        "start, end, expected",
        [
            # valid moves
            ((1, 4), (2, 4), True),
            ((0, 1), (2, 2), True),
            ((0, 6), (2, 5), True),
            ((7, 1), (5, 2), True),
            ((7, 6), (5, 5), True),
            ((1, 0), (3, 0), True),
            ((1, 0), (2, 0), True),

            # invalid moves
            ((1, 4), (4, 4), False),
            ((1, 4), (2, 3), False),
            ((1, 4), (7, 7), False),
            ((1, 4), (0, 4), False),
            ((1, 4), (1, 3), False),
            ((0, 1), (2, 3), False),
            ((0, 1), (7, 7), False),
            ((7, 1), (7, 4), False),
            ((7, 1), (6, 3), False),
            ((7, 6), (5, 4), False),
            ((7, 6), (2, 5), False),
            ((7, 6), (7, 4), False),
            ((7, 6), (6, 3), False),
            ((1, 0), (4, 0), False),
            ((1, 0), (2, 1), False),
            ((1, 0), (7, 7), False),
        ],
    )
    def test_possible_move(self, start: Square, end: Square, expected: bool):
        """Test possible moves on move 1.
        and that the method does not alter the state."""

        board = Board()
        assert board._possible_move(start, end) is expected
        assert board.state == Board().state

    @pytest.mark.parametrize(
        "start, end, expected",
        [
            # valid moves
            ((1, 4), (2, 4), True),
            ((1, 4), (3, 4), True),
            ((6, 4), (5, 4), True),
            ((6, 4), (4, 4), True),
            ((1, 0), (3, 0), True),
            ((1, 0), (2, 0), True),
            ((6, 0), (4, 0), True),
            ((6, 7), (4, 7), True),

            # invalid moves
            ((1, 4), (4, 4), False),
            ((1, 4), (2, 3), False),
            ((1, 4), (7, 7), False),
            ((1, 4), (0, 4), False),
            ((1, 4), (1, 3), False),
            ((6, 4), (3, 4), False),
            ((6, 4), (2, 4), False),
            ((6, 4), (7, 7), False),
            ((6, 0), (0, 4), False),
            ((6, 0), (1, 3), False),
            ((6, 0), (7, 7), False),
            ((6, 7), (0, 4), False),
            ((6, 7), (1, 3), False),
        ],
    )
    def test_pawn_possible_move(self, start: Square, end: Square, expected: bool):
        """Test Pawn possible moves on move 1."""

        board = Board()
        assert board._possible_pawn_move(start, end) is expected

    @pytest.mark.parametrize(
        "start, end, expected",
        [
            # Knight valid moves
            ((0, 1), (2, 0), True),
            ((0, 1), (2, 2), True),
            ((0, 6), (2, 7), True),
            ((0, 6), (2, 5), True),
            ((7, 1), (5, 0), True),
            ((7, 1), (5, 2), True),
            ((7, 6), (5, 7), True),
            ((7, 6), (5, 5), True),

            # Knight invalid moves
            ((0, 1), (1, 3), False),
            ((0, 1), (3, 3), False),
            ((0, 6), (1, 4), False),
            ((7, 1), (6, 3), False),
            ((7, 6), (6, 4), False),

            # King
            ((0, 4), (1, 4), False),
            ((0, 4), (1, 3), False),
            ((0, 4), (0, 3), False),
            ((0, 4), (2, 2), False),
            ((7, 4), (6, 3), False),
            ((7, 4), (6, 3), False),
            ((7, 4), (7, 3), False),
            ((7, 4), (6, 6), False),
        ],
    )
    def test_king_knight_possible_move(self, start: Square, end: Square, expected: bool):
        """Test King and Knight possible moves on move 1."""

        board = Board()
        assert board._possible_king_knight_move(start, end) is expected

    @pytest.mark.parametrize(
        "start, end",
        [
            ((0, 2), (2, 4)),
            ((0, 2), (2, 2)),
            ((0, 2), (1, 3)),
            ((0, 5), (2, 3)),
            ((0, 5), (2, 5)),
            ((7, 2), (5, 4)),
            ((7, 2), (5, 2)),
            ((7, 5), (5, 3)),
            ((7, 5), (5, 5)),
        ],
    )
    def test_bishop_possible_move(self, start: Square, end: Square):
        """Test Bishop possible moves on move 1."""

        board = Board()
        assert board._possible_bishop_move(start, end) is False

    @pytest.mark.parametrize(
        "start, end",
        [
            ((0, 0), (5, 0)),
            ((0, 0), (3, 3)),
            ((0, 0), (1, 0)),
            ((0, 7), (5, 7)),
            ((0, 7), (2, 5)),
            ((7, 0), (4, 0)),
            ((7, 0), (5, 2)),
            ((7, 7), (4, 7)),
            ((7, 7), (5, 5)),
        ],
    )
    def test_rook_possible_move(self, start: Square, end: Square):
        """Test Rook possible moves on move 1."""

        board = Board()
        assert board._possible_rook_move(start, end) is False

    @pytest.mark.parametrize("colour", [Colour.WHITE, Colour.BLACK])
    def test_has_legal_move(self, colour: Colour):
        """Test that there exists a legal move on move 1
        and that the method does not alter the state."""

        board = Board()
        assert board._has_legal_move(colour) is True
        assert board.state == Board().state

    @pytest.mark.parametrize("colour", [Colour.WHITE, Colour.BLACK])
    def test_king_checked(self, colour: Colour):
        board = Board()
        assert board._king_checked(colour) is False

    @pytest.mark.parametrize("colour", [Colour.WHITE, Colour.BLACK])
    def test_cannot_long_castle(self, colour: Colour, capfd: CaptureFixture):
        """Test cannot long castle on move 1 and that the method does not alter the state."""

        board = Board()
        assert board._long_castle(colour) is False
        assert board.state == Board().state

        capfd.readouterr()  # clear stdout

    @pytest.mark.parametrize("colour", [Colour.WHITE, Colour.BLACK])
    def test_cannot_short_castle(self, colour: Colour, capfd: CaptureFixture):
        """Test cannot short castle on move 1 and that the method does not alter the state."""

        board = Board()
        assert board._short_castle(colour) is False
        assert board.state == Board().state

        capfd.readouterr()  # clear stdout

    @pytest.mark.parametrize(
        "colour, expected",
        [
            (Colour.WHITE, (0, 4)),
            (Colour.BLACK, (7, 4)),
        ],
    )
    def test_find_king(self, colour: Colour, expected: Square):
        board = Board()
        assert board._find_king(colour) == expected

    def test_request_pawn_promotion_options(self, monkeypatch: MonkeyPatch, capfd: CaptureFixture):

        # mimic user inputs
        inputs = iter(["h", "p", "help", "q"])
        monkeypatch.setattr('builtins.input', lambda _: next(inputs))

        board = Board()
        assert board._request_pawn_promotion_option() == _PromotionOption.QUEEN

        capfd.readouterr()  # clear stdout

    @pytest.mark.parametrize(
        "notation, expected",
        [
            ("a1a1", ((0, 0), (0, 0))),
            ("a1b1", ((0, 0), (0, 1))),
            ("e5e8", ((4, 4), (7, 4))),
            ("h8a1", ((7, 7), (0, 0))),
            ("c1c8", ((0, 2), (7, 2))),
            ("a9", None),
            ("a1a9", None),
            ("a1a", None),
            ("a1", None),
            ("a", None),
            ("", None),
            ("a1a1a1", None),
        ],
    )
    def test_user_input_notation_to_coordinates(
        self, notation: str, expected: tuple[Square, Square] | None, capfd: CaptureFixture,
    ):
        board = Board()
        assert board._user_input_notation_to_coordinates(notation) == expected

        capfd.readouterr()  # clear stdout

    @pytest.mark.parametrize(
        "square, expected",
        [
            ((0, 0), "a1"),
            ((0, 1), "b1"),
            ((4, 4), "e5"),
            ((7, 7), "h8"),
            ((7, 0), "a8"),
            ((0, 7), "h1"),
        ],
    )
    def test_square_to_notation(self, square: Square, expected: str):
        board = Board()
        assert board._square_to_notation(square) == expected


class TestBoardOne:
    """This class provides tests for the custom board position
    `board_one` from `conftest.py`."""

    @pytest.mark.parametrize(
        "raw_input, turn, expected",
        [
            # valid moves
            ("o-o", Colour.WHITE, MoveOutcome.SUCCESS),
            ("o-o-o", Colour.BLACK, MoveOutcome.SUCCESS),
            ("d5e6", Colour.WHITE, MoveOutcome.CHECK),
            ("d5d7", Colour.WHITE, MoveOutcome.CHECK),
            ("d5f7", Colour.WHITE, MoveOutcome.CHECK),
            ("d5g8", Colour.WHITE, MoveOutcome.CHECK),
            ("d5a8", Colour.WHITE, MoveOutcome.CHECK),
            ("a8a1", Colour.BLACK, MoveOutcome.CHECK),
            ("d5e4", Colour.WHITE, MoveOutcome.SUCCESS),
            ("g8h7", Colour.BLACK, MoveOutcome.SUCCESS),

            # invalid moves
            ("o-o-o", Colour.WHITE, MoveOutcome.FAILURE),
            ("o-o", Colour.BLACK, MoveOutcome.FAILURE),
            ("e8f7", Colour.BLACK, MoveOutcome.FAILURE),  # will be under check
            ("c2c3", Colour.WHITE, MoveOutcome.FAILURE),  # blocked by knight
            ("c2c4", Colour.WHITE, MoveOutcome.FAILURE),  # blocked by knight
            ("d7d5", Colour.BLACK, MoveOutcome.FAILURE),  # blocked by queen
        ],
    )
    def test_make_move(
        self, game_one: Chess, raw_input: str, turn: Colour, expected: MoveOutcome, capfd: CaptureFixture,
    ):
        board = game_one.board
        assert board.make_move(raw_input, turn) == expected

        capfd.readouterr()  # clear stdout

    def test_white_can_short_castle_but_cannot_long_castle(self, game_one: Chess, capfd: CaptureFixture):
        """Test that white can short castle but cannot long castle;
        the state of the board is updated correctly."""

        board = game_one.board
        assert board._long_castle(Colour.WHITE) is False
        assert board._short_castle(Colour.WHITE) is True
        assert board.state[0][4] is None
        assert board.state[0][5] is not None
        assert board.state[0][6] is not None
        assert board.state[0][7] is None

        capfd.readouterr()  # clear stdout

    def test_black_can_long_castle_but_cannot_short_castle(self, game_one: Chess, capfd: CaptureFixture):
        """Test that black can long castle but cannot short castle;
        the state of the board is updated correctly."""

        board = game_one.board
        assert board._short_castle(Colour.BLACK) is False
        assert board._long_castle(Colour.BLACK) is True
        assert board.state[7][0] is None
        assert board.state[7][2] is not None
        assert board.state[7][3] is not None
        assert board.state[7][4] is None

        capfd.readouterr()  # clear stdout

    def test_en_passant_capture(self, game_one: Chess):
        """Test that a pawn can capture en passant;
        the start square is empty;
        the capturing pawn is moved to the target square;
        the captured pawn is removed from the board;
        the board is updated correctly."""

        board = game_one.board
        assert board.make_move("e5f6", Colour.WHITE) == MoveOutcome.SUCCESS
        assert board.state[4][4] is None
        assert board.state[5][5] is not None
        assert board.state[4][5] is None
        assert board.en_passant_pawn is None

    def test_possible_move_is_not_necessarily_legal(self, game_one: Chess):
        """Test that a possible move is not necessarily legal;
        the board is not updated.

        Black king could technically move to f7, but it would be under check."""

        board = game_one.board
        assert board._possible_move((7, 4), (6, 5)) is True
        assert board._legal_move((7, 4), (6, 5)) is False

    @pytest.mark.parametrize(
        "end_square_raw, end_square, user_input",
        [
            ("g8", (7, 6), "q"),
            ("g8", (7, 6), "r"),
            ("g8", (7, 6), "b"),
            ("g8", (7, 6), "n"),
            ("h8", (7, 7), "q"),
            ("h8", (7, 7), "r"),
            ("h8", (7, 7), "b"),
            ("h8", (7, 7), "n"),
        ]
    )
    def test_pawn_promotion(
        self,
        game_one: Chess,
        monkeypatch: MonkeyPatch,
        capfd: CaptureFixture,
        end_square_raw: str,
        end_square: Square,
        user_input: str,
    ):
        """Test that a pawn promotion is handled correctly;
        the pawn is removed from the board;
        the correct piece is placed on the board;
        the black king is in check after h7g8 capture and promotion
            to either a Queen or Rook."""

        monkeypatch.setattr('builtins.input', lambda _: user_input)

        board = game_one.board

        assert board.make_move(f"h7{end_square_raw}", Colour.WHITE) in {MoveOutcome.SUCCESS, MoveOutcome.CHECK}
        assert board.state[6][7] is None

        end_rank, end_file = end_square
        end_square_piece = board.state[end_rank][end_file]
        expected_promotion_piece_class = _PromotionPiece[_PromotionOption(user_input).name].value

        assert isinstance(end_square_piece, expected_promotion_piece_class)

        if end_file == 6 and user_input in {"q", "r"}:
            assert board._king_checked(Colour.BLACK)

        else:
            assert board._king_checked(Colour.BLACK) is False

        capfd.readouterr()  # clear stdout


class TestBoardTwo:
    """This class provides tests for the custom board position
    `board_two` from `conftest.py`."""

    def test_capturing_king_raises_value_error(self, game_two: Chess):
        """Test that capturing the king raises a ValueError.

        Note: capturing the king must never be an option in the game.
        If a player is in check and the game has not ended,
        it is their move, and they can get out of check."""

        board = game_two.board
        with pytest.raises(ValueError):
            board.make_move("g5f7", Colour.WHITE)

    def test_attempting_to_capture_king_with_illegal_move_does_not_raise_value_error(
        self, game_two, capfd: CaptureFixture,
    ):
        board = game_two.board
        board.make_move("f7g8", Colour.BLACK)
        assert board.make_move("c8g8", Colour.WHITE) == MoveOutcome.FAILURE

        capfd.readouterr()  # clear stdout

    def test_checkmate_sequence_of_moves(self, game_two: Chess, capfd: CaptureFixture):
        board = game_two.board

        moves = ["f7g8", "a2a3", "f2h2"]
        turns = [Colour.BLACK, Colour.WHITE, Colour.BLACK]
        outcomes = [MoveOutcome.SUCCESS, MoveOutcome.SUCCESS, MoveOutcome.CHECKMATE]

        for move, turn, outcome in zip(moves, turns, outcomes):
            assert board.make_move(move, turn) == outcome

        capfd.readouterr()  # clear stdout
