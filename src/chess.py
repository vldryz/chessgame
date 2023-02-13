"""This module provides the game class used to run the chess game."""
# ——————————————————————————————————————————— Imports ——————————————————————————————————————————— #
# Standard libraries
import sys
from contextlib import suppress

# Dependencies
from board import Board
from utils import Colour, Commands, Moves

# ———————————————————————————————————————————— Code ———————————————————————————————————————————— #


class Chess:
    def __init__(self, board: Board | None = None):
        self.board: Board = board or Board()
        self.turn: Colour = Colour.WHITE
        self.move_number: int = 1
        self.move_history: list = []

    def play(self):
        print("A game of chess begins.\n")
        print(self.board)

        while True:
            raw_input: str = self._request_input(f"{self.turn.value} to move on move {self.move_number}.\n"
                                                 f"Enter your move: ")
            processed_input: Commands | Moves = self._process_input(raw_input)

            if processed_input in Commands:
                self._handle_command(processed_input)
                continue

            if not self.board.make_move(raw_input, self.turn):
                continue

            self._increment_move()
            self._change_turn()

            print(self.board)

    def _increment_move(self):
        self.move_number += 1

    def _change_turn(self):
        self.turn = Colour.WHITE if self.turn == Colour.BLACK else Colour.BLACK

    @staticmethod
    def _request_input(prompt: str = "") -> str:
        """Requests a move from a user.

        Args:
            prompt (str): The prompt to display to the user.

        Returns:
            str: The user's input.

        """

        return input(prompt).lower()

    @staticmethod
    def _process_input(raw_input: str) -> Commands | Moves:
        """Processes a user's input.

        We use this method to request a move from the user.
        It will first try to convert the input to a command.
        If it fails, it will consider the input a move.

        Args:
            raw_input (str): The user's input.

        Returns:
            Commands | Moves: The type of input.

        """

        # in Python 3.12 it will be possible to check whether a string is
        # one of the values of an Enum instead of using a suppression method.

        with suppress(ValueError):
            return Commands(raw_input)

        return Moves.DEFAULT

    def _handle_command(self, command: Commands) -> None:
        """Handles a command input."""
        if command == Commands.HELP:
            # TODO: Add help message
            print("Help message")

        elif command == Commands.RESIGN:
            print(f"{self.turn.value} resigns. "
                  f"{Colour.WHITE.value if self.turn == Colour.BLACK else Colour.BLACK.value} wins.")
            self._after_match()

        elif command == Commands.DRAW:
            print("The match ends in a draw.")
            self._after_match()

        elif command == Commands.RESET:
            Chess().play()
            sys.exit()

        elif command == Commands.SAVE_MOVE_HISTORY:
            self._save_move_history()

        elif command == Commands.PRINT_BOARD:
            print(self.board)

        elif command == Commands.EXIT:
            print("Exiting game...")
            sys.exit()

    def _after_match(self) -> None:
        """Prompts the user end of the game options."""
        print("Would you like to play again? [yes/no].\nFor other options, type 'help'.\n")
        input_ = input().lower()

        # use _request_input() and say that must be command since the game is over. suggest printing help message

        if input_ == Commands.YES.value:
            Chess().play()
            sys.exit()

        elif input_ == Commands.NO.value:
            sys.exit()

        elif input_ == Commands.SAVE_MOVE_HISTORY.value:
            self._save_move_history()

        elif input_ == Commands.HELP.value:
            # TODO: Add help message
            print("Help message")

        else:
            print("Invalid input.\n")
            self._after_match()

    def _save_move_history(self, file_name: str = "move_history.txt") -> None:
        """Saves the move history to a `.txt` file."""
        with open(file_name, "w") as file:
            file.write(str(self.move_history))

        print(f"Move history saved in {file_name}.")
