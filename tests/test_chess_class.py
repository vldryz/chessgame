"""This module provides tests for the Chess class."""

import os
from tempfile import TemporaryDirectory

import pytest
from pytest import CaptureFixture, MonkeyPatch
from pytest_mock import MockerFixture

from chess import Chess
from chess.board import MoveOutcome


class TestDefaultChess:
    """Test the default chess game."""

    def test_move_history_is_saved_to_file(
        self, mocker: MockerFixture, monkeypatch: MonkeyPatch, capfd: CaptureFixture
    ) -> None:
        """Test that the move history is saved to a file when the user
        inputs 'save move history', and the file content after a match ends.
        """
        mocker.patch(
            "chess.board.Board.make_move",
            side_effect=[MoveOutcome.SUCCESS, MoveOutcome.SUCCESS, MoveOutcome.CHECKMATE],
        )

        with TemporaryDirectory() as temp_dir:
            inputs = iter(
                [
                    "e2e4",
                    "e7e5",
                    "b1c3",
                    "save move history",
                    "help",
                    "nonsense",
                    f"{temp_dir}/test.txt",
                    "no",
                ]
            )
            monkeypatch.setattr("builtins.input", lambda _: next(inputs))

            filename = os.path.join(temp_dir, "test.txt")

            with pytest.raises(SystemExit):
                Chess().play()

            capfd.readouterr()  # clear stdout

            assert os.path.exists(filename)
            with open(filename) as f:
                assert f.read() == "1. e2e4; 1. e7e5\n2. b1c3"

    def test_game_ended_in_checkmate_prompts_option_to_continue(
        self, mocker: MockerFixture, monkeypatch: MonkeyPatch, capfd: CaptureFixture
    ) -> None:
        mocker.patch("chess.board.Board.make_move", return_value=MoveOutcome.CHECKMATE)
        after_match_spy = mocker.patch(
            "chess.chess_class.Chess._after_match", wraps=Chess()._after_match
        )

        inputs = iter(["e2e4", "help", "no"])
        monkeypatch.setattr("builtins.input", lambda _: next(inputs))

        with pytest.raises(SystemExit) as pytest_wrapped_e:
            Chess().play()

        capfd.readouterr()  # clear stdout

        after_match_spy.assert_called_once()
        assert pytest_wrapped_e.type == SystemExit
        assert pytest_wrapped_e.value.code == 0

    def test_exit(self, monkeypatch: MonkeyPatch, capfd: CaptureFixture) -> None:
        """Test that the program exits with code 0 when the user inputs 'exit'."""
        monkeypatch.setattr("builtins.input", lambda _: "exit")

        with pytest.raises(SystemExit) as pytest_wrapped_e:
            Chess().play()

        capfd.readouterr()  # clear stdout

        assert pytest_wrapped_e.type == SystemExit
        assert pytest_wrapped_e.value.code == 0

    def test_moves_are_processed_correctly(
        self, monkeypatch: MonkeyPatch, capfd: CaptureFixture
    ) -> None:
        """Test that the program processes user input moves correctly.
        The sequence of moves leads to a checkmate of the white king on move 2.
        """
        chess = Chess()

        inputs = iter(["f2f3", "e7e5", "g2g4", "d8h4", "no"])
        monkeypatch.setattr("builtins.input", lambda _: next(inputs))

        with pytest.raises(SystemExit) as pytest_wrapped_e:
            chess.play()

        capfd.readouterr()  # clear stdout

        assert pytest_wrapped_e.type == SystemExit
        assert pytest_wrapped_e.value.code == 0
