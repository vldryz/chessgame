"""This module provides the board class used to manage the state of the chess board."""
# ——————————————————————————————————————————— Imports ——————————————————————————————————————————— #
# Standard libraries
from typing import Optional
from contextlib import suppress
from itertools import product
from enum import Enum

# Dependencies
from .pieces import *
from .colours import Colour

# ———————————————————————————————————————————— Code ———————————————————————————————————————————— #


class MoveCommands(Enum):
    """Enum class for moves."""
    SHORT_CASTLE = "o-o"
    LONG_CASTLE = "o-o-o"

    # Default command to play a move
    PIECE_MOVE = "piece move"


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
            bool: Whether the move was played. False if the move was illegal.

        """
        move = self._process_input(raw_input)

        if move == MoveCommands.SHORT_CASTLE:
            return self._short_castle(turn)

        if move == MoveCommands.LONG_CASTLE:
            return self._short_castle(turn)

        # unpacking with walrus operator is not supported
        if not (coordinates := self._notation_to_coordinates(raw_input)):
            return False

        start, end = coordinates

        if not self.move_piece(start, end, turn):
            return False

    def move_piece(self, start: tuple[int, int], end: tuple[int, int], turn: Colour) -> bool:
        """The function to process a move.

        Args:
            start (tuple[int, int]): The starting position of the piece.
            end (tuple[int, int]): The ending position of the move.
            turn (Colour): The colour of the pieces of the player making the move.

        Returns:
            bool: Whether the move was played. False if the move was illegal.

        """

        piece = self.state[start[0]][start[1]]
        if not piece:
            print(f"Invalid Move: There is no piece at {start}.\n")
            return False

        if piece.colour != turn:
            print(f"Invalid Move: It is {turn}'s turn.\n")
            return False

        if end not in piece.legal_moves(start, self):
            print(f"Invalid Move: {piece} cannot move to {end}.\n")
            return False



        self.state[end[0]][end[1]] = piece
        self.state[start[0]][start[1]] = None
        piece.moved = True

        return True

    def _short_castle(self, turn: Colour) -> bool:
        """Performs a short castle.

        Args:
            turn (Colour): The colour of the pieces of the player making the move.

        Returns:
            bool: Whether the move was played. False if the move was illegal.

        """

        file = 0 if turn == Colour.WHITE else 7

        king = self.state[file][4]
        rook = self.state[file][7]
        in_between_squares = [(file, 5), (file, 6)]

        if not isinstance(king, King) or not isinstance(rook, Rook) or king.moved or rook.moved:
            print("Invalid Move: King or Rook has been moved.\n")
            return False

        if king.checked:
            print("Invalid Move: Cannot castle under check.\n")
            return False

        for file_, rank_ in in_between_squares:
            if self.state[file_][rank_]:
                print("Invalid Move: Cannot castle through another piece.\n")
                return False

            self.state[file_][rank_] = king

            if self._king_checked(turn):
                print("Invalid Move: Cannot castle through check.\n")
                return False

        self.state[file][4] = None
        self.state[file][5] = rook
        self.state[file][6] = king
        self.state[file][7] = None

        return True

    def _long_castle(self, turn: Colour) -> bool:
        """Performs a long castle.

        Args:
            turn (Colour): The colour of the pieces of the player making the move.

        Returns:
            bool: Whether the move was played. False if the move was illegal.

        """

        file = 0 if turn == Colour.WHITE else 7

        king: Optional[King] = self.state[file][4]
        rook: Optional[Rook] = self.state[file][0]
        in_between_squares = [(file, 2), (file, 3)]
        check_for_pieces = in_between_squares + [(file, 1)]

        if king.checked:
            print(f"Invalid Move: Cannot castle under check.\n")
            return False

        if not king or not rook or king.moved or rook.moved:
            print(f"Invalid Move: King or Rook has been moved.\n")
            return False

        for square in check_for_pieces:
            if square:
                print(f"Invalid Move: Cannot castle through another piece.\n")
                return False

        self.state[file][0] = None
        self.state[file][2] = king
        self.state[file][3] = rook
        self.state[file][4] = None

        return True

    def _king_checked(self, turn: Colour) -> bool:
        """Checks whether the king of a player is checked.

        Args:
            turn (Colour): The colour of the pieces of the player making the move.

        Returns:
            bool: Whether the king is checked.

        """

        file, rank = self._find_king(turn)
        king = self.state[file][rank]

        for file_, rank_ in product(range(8), range(8)):
            piece = self.state[file_][rank_]
            if piece and piece.colour != turn:
                if (file, rank) in piece.legal_moves((file_, rank_), self):
                    return True

        return False


    def _find_king(self, turn: Colour) -> tuple[int, int]:
        """Finds the position of the king of the player.

        Args:
            turn (Colour): The colour of the pieces of the player making the move.

        Returns:
            tuple[int, int]: The coordinates of the king.

        """

        file, rank = -1, -1
        for file, rank in product(range(8), range(8)):
            piece = self.state[file][rank]
            if isinstance(piece, King) and piece.colour == turn:
                return file, rank

        return file, rank

    @staticmethod
    def _process_input(raw_input: str) -> MoveCommands:
        """Gets the type of move.

        The method first checks whether the input is a command like
        castling. If it is, it returns the corresponding move type.
        If it is not, it assumes the input is a piece move.

        Args:
            raw_input (str): The move to get the type of.

        Returns:
            MoveCommands: The type of move.

        """

        with suppress(ValueError):
            return MoveCommands(raw_input)

        return MoveCommands.PIECE_MOVE

    @staticmethod
    def _notation_to_coordinates(notation: str) -> Optional[tuple[tuple[int, int], tuple[int, int]]]:
        """Converts a chess notation to a tuple of board coordinates.

        Args:
            notation (str): The chess notation to convert.

        Returns:
            Optional[tuple[tuple[int, int], tuple[int, int]]]:
                The file and rank of the start and end squares of the move.
                None if the move is invalid.

        """

        if len(notation) != 4:
            print(f"Invalid Move: {notation} is not a valid move.\n")
            return None

        ranks = ["a", "b", "c", "d", "e", "f", "g", "h"]

        rank_start, rank_end = notation[0], notation[2]
        file_start, file_end = notation[1], notation[3]

        # Check if the start and end ranks are valid
        if not {rank_start, rank_end}.issubset(set(ranks)):
            print("Invalid Move: Rank selection is invalid.\n")
            return None

        # Check if the start and end files are valid
        if not all(
                file.isdigit() or int(file) not in range(1, 9)
                for file in {file_start, file_end}
        ):
            print("Invalid Move: File selection is invalid.\n")
            return None

        return (
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
