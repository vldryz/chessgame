class Board:
    def __init__(self):
        wr_1 = Rook('W')
        wn_1 = Knight('W')
        wb_1 = Bishop('W')
        wq = Queen('W')
        wk = King('W')
        wb_2 = Bishop('W')
        wn_2 = Knight('W')
        wr_2 = Rook('W')
        wp_1 = Pawn('W')
        wp_2 = Pawn('W')
        wp_3 = Pawn('W')
        wp_4 = Pawn('W')
        wp_5 = Pawn('W')
        wp_6 = Pawn('W')
        wp_7 = Pawn('W')
        wp_8 = Pawn('W')

        br_1 = Rook('B')
        bn_1 = Knight('B')
        bb_1 = Bishop('B')
        bq = Queen('B')
        bk = King('B')
        bb_2 = Bishop('B')
        bn_2 = Knight('B')
        br_2 = Rook('B')
        bp_1 = Pawn('B')
        bp_2 = Pawn('B')
        bp_3 = Pawn('B')
        bp_4 = Pawn('B')
        bp_5 = Pawn('B')
        bp_6 = Pawn('B')
        bp_7 = Pawn('B')
        bp_8 = Pawn('B')

        self.state = [
            [wr_1, wn_1, wb_1, wq, wk, wb_2, wn_2, wr_2],
            [wp_1, wp_2, wp_3, wp_4, wp_5, wp_6, wp_7, wp_8],
            [None] * 8,
            [None] * 8,
            [None] * 8,
            [None] * 8,
            [bp_1, bp_2, bp_3, bp_4, bp_5, bp_6, bp_7, bp_8],
            [br_1, bn_1, bb_1, bq, bk, bb_2, bn_2, br_2]
        ]

        # Keep track of the positions of both kings to aid in the detection of checks
        self.wk_pos = (0, 4)
        self.bk_pos = (7, 4)

    def update(self, start, end, update_state=True):

        start_square = self.state[start[0]][start[1]]
        end_square = self.state[end[0]][end[1]]

        self.state[end[0]][end[1]] = self.state[start[0]][start[1]]
        self.state[start[0]][start[1]] = None

        # update king's position if it moved
        if isinstance(start_square, King):
            if start_square.colour == 'W':
                self.wk_pos = end
            else:
                self.bk_pos = end

        # if a move puts king in check then undo the move
        if self.check_if_check(start_square.colour):
            self.state[end[0]][end[1]] = end_square
            self.state[start[0]][start[1]] = start_square
            return False

        # keep track of moves for king and rook for castles and of pawn for en passant
        if not update_state:
            self.state[start[0]][start[1]] = start_square
            self.state[end[0]][end[1]] = end_square
            if isinstance(start_square, Pawn) or isinstance(start_square, King) or isinstance(start_square, Rook):
                self.state[start[0]][start[1]].has_moved = start_square.has_moved
            if isinstance(start_square, Pawn):
                self.state[start[0]][start[1]].en_passant = start_square.en_passant

        # Pawn promotion
        if update_state and isinstance(start_square, Pawn) and (end[0] == 7 or end[0] == 0):
            promote = None
            while promote not in ["Q", "B", "N", "R"]:
                promote = input("Promote your pawn to Q, B, N, R:")
                if promote == "B":
                    self.state[end[0]][end[1]] = Bishop(start_square.colour)
                elif promote == "N":
                    self.state[end[0]][end[1]] = Knight(start_square.colour)
                elif promote == "R":
                    self.state[end[0]][end[1]] = Rook(start_square.colour)
                elif promote == "Q":
                    self.state[end[0]][end[1]] = Queen(start_square.colour)

        return True

    def check_if_check(self, colour):
        """
        We can check whether the king is in check or not by the following method:
        1- replace the king with bishop and check bishop's all available moves
        2- if on any move's square, there is a bishop or a queen, the king is in check
        3- repeat 1 and 2 for rook, knight and pawn
        """
        king_pos = self.wk_pos if colour == 'W' else self.bk_pos

        # replace king with bishop and check all available moves
        bishop = Bishop(colour)
        bishop.get_available_moves(king_pos, self.state)
        for square in bishop.available_moves:
            piece = self.state[square[0]][square[1]]
            if piece and (isinstance(piece, Bishop) or isinstance(piece, Queen)):
                return True

        # replace king with rook and check all moves
        rook = Rook(colour)
        rook.get_available_moves(king_pos, self.state)
        for square in rook.available_moves:
            piece = self.state[square[0]][square[1]]
            if piece and (isinstance(piece, Rook) or isinstance(piece, Queen)):
                return True

        # replace king with knight and check all moves
        knight = Knight(colour)
        knight.get_available_moves(king_pos, self.state)
        for square in knight.available_moves:
            piece = self.state[square[0]][square[1]]
            if piece and isinstance(piece, Knight):
                return True

        # replace king with pawn and check for capture moves
        multiplier = 1 if colour == 'W' else -1
        pawn_position_1 = [king_pos[0] + multiplier, king_pos[1] + 1]
        pawn_position_2 = [king_pos[0] + multiplier, king_pos[1] - 1]

        # IndexError occurs when King moves to a border
        try:
            piece_1 = self.state[pawn_position_1[0]][pawn_position_1[1]]
        except IndexError:
            piece_1 = None
        try:
            piece_2 = self.state[pawn_position_2[0]][pawn_position_2[1]]
        except IndexError:
            piece_2 = None

        if (piece_1 and piece_1.colour != colour and isinstance(piece_1, Pawn)) or \
                (piece_2 and piece_2.colour != colour and isinstance(piece_2, Pawn)):
            return True

        return False

    def is_there_a_move(self, colour):
        """
        Checks if there exists at least 1 legal move for a player
        """
        prev_wk_pos = self.wk_pos
        prev_bk_pos = self.bk_pos
        for i in range(0, 8):
            for j in range(0, 8):
                # check if piece exists on square and is of the same colour
                piece = self.state[i][j]
                if piece and piece.colour == colour:
                    # get all available moves
                    piece.get_available_moves([i, j], self.state)
                    for piece_move in piece.available_moves:
                        # if we can update the board with an available move that is
                        # used to check if a move gets the king out of check
                        if self.update([i, j], piece_move, update_state=False):
                            self.wk_pos = prev_wk_pos
                            self.bk_pos = prev_bk_pos
                            return True

                        self.wk_pos = prev_wk_pos
                        self.bk_pos = prev_bk_pos
        return False

    def short_castle(self, colour):
        if colour == 'W':
            king_pos = [0, 4]
            king = self.state[0][4]
            rook = self.state[0][7]
            in_between_squares = [[0, 5], [0, 6]]
        else:
            king_pos = [7, 4]
            king = self.state[7][4]
            rook = self.state[7][7]
            in_between_squares = [[7, 5], [7, 6]]

        # can't castle is king or rook had moved
        if not king or king.is_checked or king.has_moved or not rook or rook.has_moved:
            return False

        # can't castle if there are pieces in between or if the King has to move
        # through a square that would put it in check
        prev_wk_pos = self.wk_pos
        prev_bk_pos = self.bk_pos
        for square in in_between_squares:
            if self.state[square[0]][square[1]] or not self.update(king_pos, square, update_state=False):
                self.wk_pos = prev_wk_pos
                self.bk_pos = prev_bk_pos
                return False

        # move king and rook
        if colour == 'W':
            self.state[0][6] = self.state[0][4]
            self.state[0][4] = None
            self.wk_pos = [0, 6]

            self.state[0][5] = self.state[0][7]
            self.state[0][7] = None

        else:
            self.state[7][6] = self.state[7][4]
            self.state[7][4] = None
            self.wk_pos = [7, 6]

            self.state[7][5] = self.state[7][7]
            self.state[7][7] = None

        return True

    def long_castle(self, colour):
        if colour == 'W':
            king_pos = [0, 4]
            king = self.state[0][4]
            rook = self.state[0][0]
            in_between_squares = [[0, 2], [0, 3]]
        else:
            king_pos = [7, 4]
            king = self.state[7][4]
            rook = self.state[7][0]
            in_between_squares = [[7, 2], [7, 3]]

        # can't castle is king or rook had moved
        if not king or king.is_checked or king.has_moved or not rook or rook.has_moved:
            return False

        # can't castle if there are pieces in between or if the King has to move
        # through a square that would put it in check
        prev_wk_pos = self.wk_pos
        prev_bk_pos = self.bk_pos
        for square in in_between_squares:
            # can not castle if there are pieces in between or if the king moves through a checked square
            if self.state[square[0]][square[1]] or not self.update(king_pos, square, update_state=False):
                self.wk_pos = prev_wk_pos
                self.bk_pos = prev_bk_pos
                return False

        # move king and rook
        if colour == 'W':
            self.state[0][2] = self.state[0][4]
            self.state[0][4] = None
            self.wk_pos = [0, 2]

            self.state[0][3] = self.state[0][0]
            self.state[0][0] = None

        else:
            self.state[7][2] = self.state[7][4]
            self.state[7][4] = None
            self.wk_pos = [7, 2]

            self.state[7][3] = self.state[7][0]
            self.state[7][0] = None

        return True

    def __repr__(self):
        return "\n" + "\n".join(
            "".join(repr(piece) + " " if piece else ". " for piece in row) + " " + str(8 - col)
            for col, row in enumerate(self.state[::-1])) + "\n\n" + \
               " ".join(['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']) + "\n"


class Piece:
    def __init__(self, colour, icon):
        self.colour = colour
        self.icon = icon
        self.available_moves = []

    def __repr__(self):
        return self.icon

    def end_square_is_legal(self, end, board):
        """
        Checks if the end square contains a piece of the same colour
        """
        end_square = board[end[0]][end[1]]
        return not (end_square and end_square.colour == self.colour)


class Rook(Piece):
    def __init__(self, colour):
        super().__init__(colour, "♜" if colour == 'W' else '♖')
        self.has_moved = False

    def is_legal(self, start, end, board):
        """
        Rook can only move orthogonally if not blocked by other pieces
        Mathematically, only X or Y should change
        """
        if not super().end_square_is_legal(end, board):
            return False

        if not (start[0] == end[0] or start[1] == end[1]):
            return False

        # check all squares in between
        x_direction = y_direction = 0
        if start[0] != end[0]:
            y_direction = 1 if end[0] > start[0] else -1
        else:
            x_direction = 1 if end[1] > start[1] else -1

        for diff in range(1, abs(start[0] - end[0]) + abs(start[1] - end[1])):
            if board[start[0] + diff * y_direction][start[1] + diff * x_direction]:
                return False

        return True

    def get_available_moves(self, start, board):
        self.available_moves = []
        for i in range(0, 8):
            for j in range(0, 8):
                try:
                    if self.is_legal(start, [i, j], board):
                        self.available_moves.append([i, j])
                except IndexError:
                    # occurs when a rook is by the border
                    continue


class Knight(Piece):
    def __init__(self, colour):
        super().__init__(colour, "♞" if colour == 'W' else '♘')

    def is_legal(self, start, end, board):
        """
        Knights move one square diagonally and one move orthogonally in
        the same direction

        Mathematically a knight's move works like this:
        the difference between start and end is always some combination of (1,2)
        for e.g.
        if start is 4,4 and end is 3,6
        the difference is -1,+2 which is a combination of (1,2) so it is valid
        whereas if end is 3,5 the difference is (-1,+1) which is not valid
        the sign does not matter
        """
        if not super().end_square_is_legal(end, board):
            return False

        if not abs((start[0] - end[0]) * (start[1] - end[1])) == 2:
            return False

        return True

    def get_available_moves(self, start, board):
        self.available_moves = []
        for i in range(0, 8):
            for j in range(0, 8):
                if self.is_legal(list(start), [i, j], board):
                    self.available_moves.append([i, j])


class Bishop(Piece):
    def __init__(self, colour):
        super().__init__(colour, "♝" if colour == 'W' else '♗')

    def is_legal(self, start, end, board):
        """
        Bishop can only move diagonally if not blocked by other pieces
        Mathematically, both X and Y should have same difference
        """
        if not super().end_square_is_legal(end, board):
            return False

        if abs(start[0] - end[0]) != abs(start[1] - end[1]):
            return False

        # check all squares in between
        y_direction = 1 if end[0] > start[0] else -1
        x_direction = 1 if end[1] > start[1] else -1

        for diff in range(1, abs(start[0] - end[0])):
            if board[start[0] + diff * y_direction][start[1] + diff * x_direction]:
                return False

        return True

    def get_available_moves(self, start, board):
        self.available_moves = []
        for i in range(0, 8):
            for j in range(0, 8):
                try:
                    if self.is_legal(start, [i, j], board):
                        self.available_moves.append([i, j])
                except IndexError:
                    # occurs when a bishop is by the border
                    continue


class Queen(Piece):
    def __init__(self, colour):
        super().__init__(colour, "♛" if colour == 'W' else '♕')

    def is_legal(self, start, end, board):
        """
        Queen can move diagonally and orthogonally
        basically a bishop or a rook move
        """
        if not super().end_square_is_legal(end, board):
            return False

        rook = Rook(self.colour)
        bishop = Bishop(self.colour)

        if not (rook.is_legal(start, end, board) or bishop.is_legal(start, end, board)):
            return False

        return True

    def get_available_moves(self, start, board):
        self.available_moves = []
        for i in range(0, 8):
            for j in range(0, 8):
                if self.is_legal(start, [i, j], board):
                    self.available_moves.append([i, j])


class King(Piece):
    def __init__(self, colour):
        super().__init__(colour, "♚" if colour == 'W' else '♔')
        self.is_checked = False
        self.has_moved = False

    def is_legal(self, start, end, board):
        """
        King can move one square in any direction that is not in check
        """
        if not super().end_square_is_legal(end, board):
            return False

        if not (abs(start[0] - end[0]) <= 1 and abs(start[1] - end[1]) <= 1):
            return False

        return True

    def get_available_moves(self, start, board):
        self.available_moves = []

        for i in range(0, 8):
            for j in range(0, 8):
                if self.is_legal(start, [i, j], board):
                    self.available_moves.append([i, j])


class Pawn(Piece):
    def __init__(self, colour):
        self.has_moved = False
        self.en_passant = False  # tracks whether a pawn can be captured using en passant
        super().__init__(colour, "♟" if colour == 'W' else '♙')

    def is_legal(self, start, end, board, is_test=False):
        if not super().end_square_is_legal(end, board):
            return False

        if self.colour == 'W':
            diff_multiplier = 1
        else:
            diff_multiplier = -1

        # first move of a pawn can move up to two squares. Becomes available for en passant
        if start[1] == end[1] and (end[0] - start[0]) * diff_multiplier == 2 and not self.has_moved and \
                not board[end[0]][end[1]] and not board[end[0] - diff_multiplier][end[1]]:
            self.en_passant = True
            return True

        # the pawn moves one step further
        elif start[1] == end[1] and (end[0] - start[0]) * diff_multiplier == 1 and not board[end[0]][end[1]]:
            return True

        # capture, including en passant
        elif board[end[0]][end[1]] or (isinstance(board[end[0] - diff_multiplier][end[1]], Pawn) and board[
            end[0] - diff_multiplier][end[1]].colour != self.colour and board[
                                           end[0] - diff_multiplier][end[1]].en_passant):

            # there is a piece at end position then check if valid capture
            if abs(start[1] - end[1]) == (end[0] - start[0]) * diff_multiplier == 1:
                if not is_test and (end[0] == 5 or end[0] == 2):
                    board[end[0] - diff_multiplier][end[1]] = None
                return True

        return False

    def get_available_moves(self, start, board):
        self.available_moves = []
        for i in range(0, 8):
            for j in range(0, 8):
                try:
                    if self.is_legal(start, [i, j], board, is_test=True):
                        self.available_moves.append([i, j])
                except IndexError:
                    # occurs because of is_legal when a pawn in by the border
                    continue


class Game:
    def __init__(self):
        self.turn = 'W'  # W if white's turn, B if Black's turn
        self.move_number = 1
        self.board = Board()
        self.temp_pawn_pos = None

    def increment_move(self):
        self.move_number += 1

    def change_turn(self):
        self.turn = 'W' if self.turn == 'B' else 'B'

    @staticmethod
    def notation_to_coordinates(notation):
        ranks = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']

        rank = notation[0]
        file = notation[1]

        if rank not in ranks:
            print(f"Invalid Move: Rank {rank} does not exist")
            return False

        if not file.isdigit() or int(file) not in range(1, 9):
            print(f"Invalid Move: File {file} does not exist")
            return False

        return int(file) - 1, ranks.index(rank)

    def move(self, move_notation):

        if move_notation == "O-O":
            if self.board.short_castle(self.turn):
                return True
        elif move_notation == "O-O-O":
            if self.board.long_castle(self.turn):
                return True

        if len(move_notation) != 4:
            print("Invalid Move: Please enter a legal move!")
            return False

        start_notation = move_notation[:2]
        end_notation = move_notation[2:]

        start_pos = self.notation_to_coordinates(start_notation)
        if not start_pos:
            return False

        end_pos = self.notation_to_coordinates(end_notation)
        if not end_pos:
            return False

        piece_to_move = self.board.state[start_pos[0]][start_pos[1]]

        if not piece_to_move:
            print(f"Invalid Move: No piece exists at {start_notation}")
            return False

        if piece_to_move.colour != self.turn:
            print(f"Invalid Move: It is {'White' if self.turn == 'W' else 'Black'}'s turn")
            return False

        if not piece_to_move.is_legal(start_pos, end_pos, self.board.state):
            print(f"Invalid move for {piece_to_move}")
            return False

        prev_wk_pos = self.board.wk_pos
        prev_bk_pos = self.board.bk_pos

        if not self.board.update(start_pos, end_pos):
            self.board.wk_pos = prev_wk_pos
            self.board.bk_pos = prev_bk_pos
            print("Invalid Move! The king will be or is in check")
            return False

        print(str(self.move_number) + ". " + str(piece_to_move) + end_notation)

        if hasattr(piece_to_move, 'has_moved') and not piece_to_move.has_moved:
            piece_to_move.has_moved = True

        # track pawn for en passant
        if self.temp_pawn_pos:
            piece = self.board.state[self.temp_pawn_pos[0]][self.temp_pawn_pos[1]]
            if piece and isinstance(piece, Pawn) and piece.colour != self.turn:
                # the pawn was not captured:
                piece.en_passant = False
                self.temp_pawn_pos = None

        if isinstance(piece_to_move, Pawn):
            if piece_to_move.en_passant:
                self.temp_pawn_pos = end_pos

        return True
