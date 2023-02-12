"""This module provides the board class used to manage the state of the chess board."""
# ——————————————————————————————————————————— Imports ——————————————————————————————————————————— #
# Dependencies
from pieces import *
from utils import Colour

# ———————————————————————————————————————————— Code ———————————————————————————————————————————— #


class Board:
    """Class used to manage the state of the chess board."""
    def __init__(self):
        self.state: list[list[Rook | Knight | Bishop | King | Queen | Pawn | None]] = [
            [
                Rook(Colour.WHITE),
                Knight(Colour.WHITE),
                Bishop(Colour.WHITE),
                Queen(Colour.WHITE),
                King(Colour.WHITE),
                Bishop(Colour.WHITE),
                Knight(Colour.WHITE),
                Rook(Colour.WHITE),
            ],
            [Pawn(Colour.WHITE) for _ in range(8)],
            [None] * 8,
            [None] * 8,
            [None] * 8,
            [None] * 8,
            [Pawn(Colour.BLACK) for _ in range(8)],
            [
                Rook(Colour.BLACK),
                Knight(Colour.BLACK),
                Bishop(Colour.BLACK),
                Queen(Colour.BLACK),
                King(Colour.BLACK),
                Bishop(Colour.BLACK),
                Knight(Colour.BLACK),
                Rook(Colour.BLACK),
            ],
        ]

    def make_move(self, raw_input: str, turn: Colour) -> bool:
        """Makes a move on the board.

        Args:
            raw_input (tuple[int, int]): The move to make.
            turn (Colour): The colour of the pieces of the player making the move.

        Returns:
            bool: Whether the move was legal.

        """
        ...

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

    def __str__(self):
        return (
            (
                (
                    "\n"
                    + "\n".join(
                        "".join(f"{piece} " if piece else ". " for piece in row)
                        + " "
                        + str(8 - col)
                        for col, row in enumerate(self.state[::-1])
                    )
                )
                + "\n\n"
            )
            + " ".join(["a", "b", "c", "d", "e", "f", "g", "h"])
            + "\n"
        )
