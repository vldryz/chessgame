"""This module provides the game class used to run the chess game."""
# ——————————————————————————————————————————— Imports ——————————————————————————————————————————— #
# Standard libraries
import sys

# Dependencies
from board import Board
from utils import Colour, InputType, Commands

# ———————————————————————————————————————————— Code ———————————————————————————————————————————— #


class Chess:
    def __init__(self, board: Board | None = None):
        self.board: Board = board or Board()
        self.turn: Colour = Colour.WHITE
        self.move_number: int = 1
        self.move_history: list = []

    def play(self):
        print("A game of chess begins.")
        print(self.board)

        while True:
            input_, input_type = self._request_input(f"{self.turn.value} to move on move {self.move_number}.\n"
                                                     f"Enter your move: ")

            if input_type == InputType.COMMAND:  # process command
                self._handle_command(input_)
                continue

            success, start, end = self._handle_move(input_)  # process move
            if not success:  # if the move was invalid, ask for another move
                continue

            if not self.board.make_move(start, end):  # if the move was illegal, ask for another move
                continue

            print(self.board)

    def _increment_move(self):
        self.move_number += 1

    def _change_turn(self):
        self.turn = Colour.WHITE if self.turn == Colour.BLACK else Colour.BLACK

    @staticmethod
    def _request_input(prompt) -> tuple[str, InputType]:
        """Requests a move from a user.

        Args:
            prompt (str): The prompt to display to the user.

        Returns:
            tuple[str, InputType]: The user's input and the type of input.

        """

        input_ = input(prompt).lower()

        # In Python 3.12 it will be possible to check for member values in enums with "in `class_name`".
        # https://docs.python.org/3/library/enum.html#data-types
        return (input_, InputType.COMMAND) if input_ in Commands.values() else (input_, InputType.MOVE)

    def _handle_command(self, input_: str) -> None:
        """Handles a command input."""
        if input_ == Commands.HELP:
            # TODO: Add help message
            print("Help message")

        elif input_ in {Commands.SURRENDER.value, Commands.RESIGN.value}:
            print(f"{self.turn.value} resigns. "
                  f"{Colour.WHITE.value if self.turn == Colour.BLACK else Colour.BLACK.value} wins.")
            self._after_match()

        elif input_ == Commands.DRAW.value:
            print("The match ends in a draw.")
            self._after_match()

        elif input_ == Commands.RESET.value:  # reset the game
            Chess().play()
            sys.exit()

        elif input_ == Commands.SAVE_MOVE_HISTORY.value:
            self._save_move_history()

        elif input_ == Commands.PRINT_BOARD.value:
            print(self.board)

        elif input_ == Commands.EXIT.value:  # terminate the programme
            print("Exiting game...")
            sys.exit()

    @staticmethod
    def _handle_move(notation: str) -> tuple[bool, tuple[int, int], tuple[int, int]]:
        """Converts a chess notation to a tuple of board coordinates.

        Args:
            notation (str): The chess notation to convert.

        Returns:
            tuple[bool, tuple[int, int], tuple[int, int]]:
                A tuple containing a boolean indicating if the conversion was
                successful, the file and rank of the square.

        """

        if len(notation) != 4:
            print(f"Invalid Move: {notation} is not a valid move.\n")
            return False, (-1, -1), (-1, -1)

        ranks = ["a", "b", "c", "d", "e", "f", "g", "h"]

        rank_start, rank_end = notation[0], notation[2]
        file_start, file_end = notation[1], notation[3]

        # Check if the start and end ranks are valid
        if not {rank_start, rank_end}.issubset(set(ranks)):
            print("Invalid Move: Rank selection is invalid.\n")
            return False, (-1, -1), (-1, -1)

        # Check if the start and end files are valid
        if not all(
            file.isdigit() or int(file) not in range(1, 9)
            for file in (file_start, file_end)
        ):
            print("Invalid Move: File selection is invalid.\n")
            return False, (-1, -1), (-1, -1)

        return (
            True,
            (int(file_start) - 1, ranks.index(rank_start)),
            (int(file_end) - 1, ranks.index(rank_end)),
        )

    def _after_match(self) -> None:
        """Prompts the user end of the game options."""
        print("Would you like to play again? [yes/no].\nFor other options, type 'help'.\n")
        input_ = input().lower()

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

    def _save_move_history(self, file_name: str = "move_history.txt"):
        """Saves the move history to a `.txt` file."""
        with open(file_name, "w") as file:
            file.write(str(self.move_history))

        print(f"Move history saved in {file_name}.")
