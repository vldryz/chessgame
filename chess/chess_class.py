"""This module provides the game class used to run the chess game."""
# ——————————————————————————————————————————— Imports ——————————————————————————————————————————— #
# Standard libraries
import sys
from typing import Self
from enum import StrEnum

# Dependencies
from chess.board import Board, MoveOutcome
from chess.colour_and_aliases import Colour
from chess.user_interaction import request_input

# ———————————————————————————————————————————— Code ———————————————————————————————————————————— #


class _GameCommand(StrEnum):
    """Enum class for commands."""

    YES = "yes"
    NO = "no"
    EXIT = "exit"
    SAVE_MOVE_HISTORY = "save move history"
    RESET = "reset"
    RESIGN = "resign"
    DRAW = "draw"
    PRINT_BOARD = "print board"
    ABORT = "abort"
    HELP = "help"
    MOVE = "move"  # Default command to play a move
    LOAD = "load"  # Implement in the future

    @classmethod
    def _missing_(cls, value: str) -> Self:
        return cls.MOVE


class Chess:
    def __init__(self, board: Board | None = None):
        self.board: Board = board or Board()
        self.turn: Colour = Colour.WHITE
        self.move_number: int = 1
        self.move_history: list[str] = []

    def play(self):
        print("A game of chess begins.", end="\n\n")
        print(self.board)

        while True:
            raw_input = request_input(
                f"{self.turn} to move on move {self.move_number}.\n"
                f"Enter your move: "
            )

            if (command := _GameCommand(raw_input)) != _GameCommand.MOVE:
                self._handle_game_command(command)
                continue

            if (outcome := self.board.make_move(raw_input, self.turn)) == MoveOutcome.FAILURE:
                continue

            self.move_history.append(f"{self.move_number}. {raw_input}")
            self._handle_move_outcome(outcome)

            # End of turn actions
            self.move_number += 1 if self.turn == Colour.BLACK else 0
            self.turn = ~self.turn

            print(self.board)

    def _handle_game_command(self, command: _GameCommand) -> None:
        """Handles a command input."""
        if command == _GameCommand.HELP:
            print(
                "Input Options:",
                "- a move in the format 'start_square + end_square', "
                "e.g. 'e2e4' to move a piece.",
                "- 'o-o' to short castle.",
                "- 'o-o-o' to long castle.",
                "- 'exit' to exit the game.",
                "- 'reset' to start a new game.",
                "- 'resign' to resign from the game.",
                "- 'draw' to end the game in a draw.",
                "- 'print board' to print the board.",
                sep="\n",
                end="\n\n",
            )

        elif command == _GameCommand.RESIGN:
            print(f"{self.turn} resigned. {~self.turn} wins.")
            self._after_match()

        elif command == _GameCommand.DRAW:
            print("The match ends in a draw.")
            self._after_match()

        elif command == _GameCommand.RESET:
            Chess().play()
            sys.exit(1)

        elif command == _GameCommand.PRINT_BOARD:
            print(self.board)

        elif command == _GameCommand.EXIT:
            print("Exiting game...")
            sys.exit(0)

        else:
            print(
                "Invalid input.",
                "For a list of commands, type 'help'.",
                sep="\n",
                end="\n\n"
            )

    def _after_match(self) -> None:
        """Prompts the user end of the game options."""
        while True:
            command = _GameCommand(
                request_input(
                    "Would you like to play again? [yes/no].\n"
                    "For other options, type 'help': "
                )
            )

            if command == _GameCommand.YES:
                Chess().play()
                sys.exit(1)

            elif command == _GameCommand.NO:
                print("Exiting game...")
                sys.exit(0)

            elif command == _GameCommand.SAVE_MOVE_HISTORY:
                self._save_move_history()
                continue

            elif command == _GameCommand.HELP:
                print(
                    "Input Options:",
                    "- 'yes' to play again.",
                    "- 'no' to exit the game.",
                    "- 'save move history' to save the move history.",
                    sep="\n", end="\n\n",
                )
                continue

            else:
                print(
                    "Invalid input."
                    "For a list of commands, type 'help'.",
                    sep="\n", end="\n\n"
                )
                continue

    def _handle_move_outcome(self, outcome: MoveOutcome) -> None:
        """Handles the outcome of a move.

        Args:
            outcome (MoveOutcome): The outcome of the move.

        """

        if outcome in MoveOutcome.GAME_OVER:
            print(f"The game has ended in a {outcome}.")

            if outcome == MoveOutcome.CHECKMATE:
                print(f"{~self.turn}'s King got checkmated. {self.turn} wins.", end="\n\n")

            self._after_match()

        if outcome == MoveOutcome.CHECK:
            print(f"{~self.turn}'s King is in check.", end="\n\n")

    def _save_move_history(self) -> None:
        """Saves the move history in a `.txt` file."""

        if not self.move_history:
            print("There is no move history to save.")
            return

        while True:
            file_name = request_input("Enter the file name: ")

            if file_name.endswith(".txt"):
                break

            if (command := _GameCommand(file_name)) == _GameCommand.HELP:
                print(
                    "Input Options:",
                    "- a file name with the '.txt' extension.",
                    "- 'abort' to abort the operation.",
                    "- 'exit' to exit the game.",
                    sep="\n", end="\n\n",
                )
                continue

            elif command == _GameCommand.ABORT:
                return

            elif command == _GameCommand.EXIT:
                print("Exiting game...")
                sys.exit(0)

            print(
                "The file extension must be '.txt'.",
                "For other options, type 'help'.",
                sep="\n", end="\n\n",
            )

        grouped_list = [self.move_history[i: i + 2] for i in range(0, len(self.move_history), 2)]
        formatted_moves = "\n".join("; ".join(pair) for pair in grouped_list)

        with open(file_name, "w") as file:
            file.write(formatted_moves)

        print(f"Move history saved in {file_name}.")
