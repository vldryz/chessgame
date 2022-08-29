# Chess in python

## Installation

1. Clone the repo
   ```sh
   git clone https://github.com/vldryz/chessgame.git
   ```
2. Create a virtual environment
   ```sh
   virtualenv <my_env_name>
   source <my_env_name>/bin/activate
   ```
3. Install required packages
   ```sh
   pip install -r requirements.txt
   ```

## How to play
1. Run *main.py* in ternimal or an IDE of your choice.
   
    ![Chess board](/Screenshots_for_readme/chess_board_default.png "Chess board")   
2. To move a piece please enter start position + end position. For example, 'e2e4' will move the e2 pawn to e4.

    ![Chess board](/Screenshots_for_readme/chess_board_e2e4.png "Chess board")

    Then, if Black wants to respond with Nc6 move, they should type 'b8c6'.

    ![Chess board](/Screenshots_for_readme/chess_board_b8c6.png "Chess board")
3. If a player wants to play short castle, type: 'O-O' \
   If a player wants to play long castle, type: 'O-O-O'
4. The game ends when a player gets checkmated or in a stalemate if a player has no available legal moves.
5. The fifty-move rule nor the repetition of moves that lead to a draw are not accounted for in this version. However, en passant move is possible.

## Core files
* *Chess_classes.py* contains the classes used in the project. For instance, Game, Board, Piece, King, Queen, Rook, Bishop, Knight, Pawn.

* *main.py* is the main runnable file used to execute the game.

* *test_Chess_classes.py* in the *test* folder contains unit tests written to test the functionality of the classes in the *Chess_classes.py* file. The tests are written with the help of the *pytest* package.

## Opportunities for further improvement
In addition to the implementation of the fifty-move rule and the repetition of moves that lead to a draw, it would be more realistic and closer to traditional chess to make the code understand formal chess moves such as Nf3, Qxb5, Rab6, Bd3+. An even better solution would be to create an interface where a player would be able to drag pieces themselves.

Since data on the state of a game is always available to us, it is possible to build a chess engine with reinforcement learning algorithm. For example, a Neural Network. If trained, it can be used to play for one of the players.