"""This module provides the board class used to manage the state of the chess board."""
# ——————————————————————————————————————————— Imports ——————————————————————————————————————————— #
# Standard libraries
from typing import Self
from itertools import product
from enum import StrEnum, Enum

# Dependencies
from chess.pieces import Pawn, King, Knight, Rook, Bishop, Queen
from chess.colour import Colour
from chess.user_interaction import request_input

# ———————————————————————————————————————————— Code ———————————————————————————————————————————— #


Square = tuple[int, int]


class MoveCommand(StrEnum):
    """Enum class for moves."""
    SHORT_CASTLE = "o-o"
    LONG_CASTLE = "o-o-o"
    PIECE_MOVE = "piece move"  # Default command to play a move

    @classmethod
    def _missing_(cls, value: str) -> Self:
        return cls.PIECE_MOVE


class PromotionOption(StrEnum):
    """Enum class for promotion options."""
    QUEEN = "q"
    ROOK = "r"
    KNIGHT = "k"
    BISHOP = "b"
    HELP = "help"
    INVALID = "INVALID"  # Default value for invalid commands

    @classmethod
    def _missing_(cls, value: str) -> Self:
        return cls.INVALID


class PromotionPiece(Enum):
    """Enum class for promotion piece types."""
    KNIGHT = Knight
    ROOK = Rook
    BISHOP = Bishop
    QUEEN = Queen


class Board:
    """Class used to manage the state of the chess board."""

    def __init__(self):
        self.state: list[list[Pawn | King | Knight | Rook | Bishop | Queen | None]] = [
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
            raw_input (Square): The move to make.
            turn (Colour): The colour of the pieces of the player making the move.

        Returns:
            bool: Whether the move was played. False otherwise.

        """

        if (move := MoveCommand(raw_input)) == MoveCommand.SHORT_CASTLE:
            return self._short_castle(turn)

        if move == MoveCommand.LONG_CASTLE:
            return self._short_castle(turn)

        # unpacking with walrus operator is not supported
        if not (coordinates := self._user_input_notation_to_coordinates(raw_input)):
            return False

        start, end = coordinates

        if not self._move_piece(start, end, turn):
            return False

    def _move_piece(self, start: Square, end: Square, turn: Colour) -> bool:
        """The function to process a move.

        Args:
            start (Square): The starting position of the piece.
            end (Square): The ending position of the move.
            turn (Colour): The colour of the pieces of the player making the move.

        Returns:
            bool: Whether the move was played. False otherwise.

        """

        start_rank, start_file = start
        end_rank, end_file = end

        piece = self.state[start_rank][start_file]
        if not piece:
            print(f"Invalid Move: There is no piece at {self._square_coordinates_to_notation(start)}.\n")
            return False

        if piece.colour != turn:
            print(f"Invalid Move: It is {turn}'s turn.\n")
            return False

        if not self._legal_move(start, end):
            print(f"Invalid Move: {piece} cannot move to {self._square_coordinates_to_notation(end)}.\n")
            return False

        self.state[end_rank][end_file] = piece
        self.state[start_rank][start_file] = None
        piece.moved = True

        if isinstance(piece, Pawn) and end_rank == 7 if turn == Colour.WHITE else 0:
            self._pawn_promotion(end, turn)

        return True

    def _legal_move(self, start: Square, end: Square) -> bool:
        """Checks whether a move is legal.

        Args:
            start (Square): The starting position of the piece.
            end (Square): The ending position of the move.

        Returns:
            bool: Whether the move is legal.

        """

        piece = self.state[start[0]][start[1]]

        if isinstance(piece, Pawn):
            return self._legal_pawn_move(piece, start, end)

        if isinstance(piece, Knight):
            return self._legal_knight_move(piece, start, end)

        if isinstance(piece, Bishop):
            return self._legal_bishop_move(piece, start, end)

        if isinstance(piece, Rook):
            return self._legal_rook_move(piece, start, end)

        if isinstance(piece, King):
            return self._legal_king_move(piece, start, end)

        return self._legal_queen_move(piece, start, end)

    def _legal_pawn_move(self, piece: Pawn, start: Square, end: Square) -> bool:
        """Checks whether a pawn move is legal.

        Args:
            piece (Pawn): The pawn to move.
            start (Square): The starting position of the piece.
            end (Square): The ending position of the move.

        Returns:
            bool: Whether the move is legal.

        """

        if end not in piece.possible_moves(start):
            return False

        start_rank, start_file = start
        end_rank, end_file = end

        diff = 1 if piece.colour == Colour.WHITE else -1

        if self.state[end_rank][end_file]:
            if abs(start_rank - end_rank) == 1 and abs(start_file - end_file) == 1:
                return True

        else:
            if start_rank == end_rank:
                if start_file == 1 and end_file == 3:
                    return True
                if start_file == 6 and end_file == 4:
                    return True
                if abs(start_file - end_file) == 1:
                    return True

        return False

    def _king_checked(self, turn: Colour) -> bool:
        """Checks whether the king of a player is checked.

        Args:
            turn (Colour): The colour of the pieces of the player making the move.

        Returns:
            bool: Whether the king is checked.

        """

        king_rank, king_file = self._find_king(turn)

        for rank_, file_ in product(range(8), range(8)):
            piece = self.state[rank_][file_]
            if piece and piece.colour != turn:
                if (king_rank, king_file) in self._legal_move((rank_, file_)):
                    return True

        return False

    def _short_castle(self, turn: Colour) -> bool:
        """Performs a short castle.

        Args:
            turn (Colour): The colour of the pieces of the player making the move.

        Returns:
            bool: Whether the move was played. False if the move was illegal.

        """

        rank = 0 if turn == Colour.WHITE else 7

        king = self.state[rank][4]
        rook = self.state[rank][7]
        in_between_squares = [(rank, 5), (rank, 6)]

        if (
            not isinstance(king, King)
            or not isinstance(rook, Rook)
            or king.moved
            or rook.moved
        ):
            print("Invalid Move: King or Rook has been moved.\n")
            return False

        if king.checked:
            print("Invalid Move: Cannot castle under check.\n")
            return False

        for rank_, file_ in in_between_squares:
            if self.state[rank_][file_]:
                print("Invalid Move: Cannot castle through another piece.\n")
                return False

            self.state[rank_][file_] = king

            if self._king_checked(turn):
                print("Invalid Move: Cannot castle through check.\n")
                return False

        self.state[rank][4] = None
        self.state[rank][5] = rook
        self.state[rank][6] = king
        self.state[rank][7] = None

        return True

    def _long_castle(self, turn: Colour) -> bool:
        """Performs a long castle.

        Args:
            turn (Colour): The colour of the pieces of the player making the move.

        Returns:
            bool: Whether the move was played. False if the move was illegal.

        """

        rank = 0 if turn == Colour.WHITE else 7

        king: King | None = self.state[rank][4]
        rook: Rook | None = self.state[rank][0]
        in_between_squares = [(rank, 2), (rank, 3)]
        check_for_pieces = in_between_squares + [(rank, 1)]

        if (
            not isinstance(king, King)
            or not isinstance(rook, Rook)
            or king.moved
            or rook.moved
        ):
            print("Invalid Move: King or Rook has been moved.\n")
            return False

        if king.checked:
            print("Invalid Move: Cannot castle under check.\n")
            return False

        for rank_, file_ in check_for_pieces:
            if self.state[rank_][file_]:
                print(f"Invalid Move: Cannot castle through another piece.\n")
                return False

        # TODO: king is left there
        for rank_, file_ in in_between_squares:
            self.state[rank_][file_] = king

            if self._king_checked(turn):
                print("Invalid Move: Cannot castle through check.\n")
                return False

        self.state[rank][0] = None
        self.state[rank][2] = king
        self.state[rank][3] = rook
        self.state[rank][4] = None

        return True

    def _find_king(self, turn: Colour) -> Square:
        """Finds the position of the king of the player.

        Args:
            turn (Colour): The colour of the pieces of the player making the move.

        Returns:
            Square: The coordinates of the king.

        """

        rank, file = -1, -1
        for rank, file in product(range(8), range(8)):
            piece = self.state[rank][file]
            if isinstance(piece, King) and piece.colour == turn:
                return rank, file

        return rank, file

    def _pawn_promotion(self, end: Square, turn: Colour) -> None:
        """This function handles pawn promotion."""
        rank, file = end

        while True:
            option = PromotionOption(request_input("Pick a piece to promote to (q/r/b/n):"))

            if option == PromotionOption.INVALID:
                print("Please select a valid promotion option.\n"
                      "Type 'help' for help message.")
                continue

            # TODO: add a help message
            if option == PromotionOption.HELP:
                print("help message")
                continue

            break

        self.state[rank][file] = PromotionPiece[option.name].value(turn)

    @staticmethod
    def _user_input_notation_to_coordinates(notation: str) -> tuple[Square, Square] | None:
        """Converts a chess notation to a tuple of board coordinates.

        Args:
            notation (str): The chess notation to convert.

        Returns:
            Optional[tuple[Square, Square]]:
                The rank and file of the start and end squares of the move.
                None if the move is invalid.

        """

        if len(notation) != 4:
            print(f"Invalid Move: {notation} is not a valid move.\n")
            return None

        files = ["a", "b", "c", "d", "e", "f", "g", "h"]

        file_start, file_end = notation[0], notation[2]
        rank_start, rank_end = notation[1], notation[3]

        # Check if the start and end ranks are valid
        if not {file_start, file_end}.issubset(set(files)):
            print("Invalid Move: File selection is invalid.\n"
                  "Type 'help' for help message.")
            return None

        # Check if the start and end files are valid
        if not all(
            rank.isdigit() or int(rank) not in range(1, 9)
            for rank in {rank_start, rank_end}
        ):
            print("Invalid Move: Rank selection is invalid.\n"
                  "Type 'help' for help message.")
            return None

        return (
            (int(rank_start) - 1, files.index(file_start)),
            (int(rank_end) - 1, files.index(file_end)),
        )

    @staticmethod
    def _square_coordinates_to_notation(square: Square) -> str:
        """Converts a square's coordinates to chess notation.

        Args:
            square (Square): The coordinates of the square.

        Returns:
            str: The square's coordinates in chess notation.

        """

        files = ["a", "b", "c", "d", "e", "f", "g", "h"]
        return files[square[1]] + str(square[0] + 1)

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
