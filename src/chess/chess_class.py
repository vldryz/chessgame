"""This module provides the game class used to run the chess game."""
# ——————————————————————————————————————————— Imports ——————————————————————————————————————————— #
# Standard libraries
import sys
from typing import Self
from enum import StrEnum

# Dependencies
from chess.board import Board
from chess.colours import Colour
from chess.user_interaction import request_input

# ———————————————————————————————————————————— Code ———————————————————————————————————————————— #


class GameCommands(StrEnum):
    """Enum class for commands."""
    YES = "yes"
    NO = "no"
    HELP = "help"
    EXIT = "exit"
    SAVE_MOVE_HISTORY = "save move history"
    RESET = "reset"
    RESIGN = "resign"
    DRAW = "draw"
    PRINT_BOARD = "print board"
    MISSING = "missing"  # Default value for missing commands
    MOVE = "move"  # Default command to play a move
    LOAD = "load"  # Implement in the future

    @classmethod
    def _missing_(cls, value: str) -> Self:
        return cls.MISSING


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
            raw_input = request_input(f"{self.turn.value} to move on move {self.move_number}.\n"
                                      f"Enter your move: ")
            command = GameCommands(raw_input)

            if command != GameCommands.MOVE:
                self._handle_game_command(command)
                continue

            if not self.board.make_move(raw_input, self.turn):
                continue

            # End of turn actions
            self._increment_move()
            self._change_turn()

            print(self.board)

    def _increment_move(self):
        self.move_number += 1

    def _change_turn(self):
        self.turn = Colour.WHITE if self.turn == Colour.BLACK else Colour.BLACK

    def _handle_game_command(self, command: GameCommands) -> None:
        """Handles a command input."""
        if command == GameCommands.HELP:
            # TODO: Add help message
            print("Help message")

        elif command == GameCommands.RESIGN:
            print(f"{self.turn.value} resigns. "
                  f"{Colour.WHITE.value if self.turn == Colour.BLACK else Colour.BLACK.value} wins.")
            self._after_match()

        elif command == GameCommands.DRAW:
            print("The match ends in a draw.")
            self._after_match()

        elif command == GameCommands.RESET:
            Chess().play()
            sys.exit()

        elif command == GameCommands.SAVE_MOVE_HISTORY:
            self._save_move_history()

        elif command == GameCommands.PRINT_BOARD:
            print(self.board)

        elif command == GameCommands.EXIT:
            print("Exiting game...")
            sys.exit()

    def _after_match(self) -> None:
        """Prompts the user end of the game options."""
        print("Would you like to play again? [yes/no].\nFor other options, type 'help'.\n")
        input_ = input().lower()

        # use _request_input() and say that must be command since the game is over. suggest printing help message

        if input_ == GameCommands.YES.value:
            Chess().play()
            sys.exit()

        elif input_ == GameCommands.NO.value:
            sys.exit()

        elif input_ == GameCommands.SAVE_MOVE_HISTORY.value:
            self._save_move_history()

        elif input_ == GameCommands.HELP.value:
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
